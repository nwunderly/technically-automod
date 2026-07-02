import json
import logging
import os
import re
import time
from urllib.parse import unquote, urlparse

import aiohttp

URL_PATTERN = re.compile(
    r"https?:\/\/+(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)

REMOVE_EXTRA_SLASHES = re.compile(
    r"(https?://)/+"
)  # remove everything not inside group

FISHFISH_API = "https://api.fishfish.gg/v1/domains"
SHORTENERS_URL = "https://raw.githubusercontent.com/nwunderly/ouranos/refs/heads/master/shorteners.txt"

logger = logging.getLogger("technically_automod")


def load_config():
    if not os.path.exists("config.json"):
        return []

    with open("config.json", "r") as f:
        text = f.read()
        if not text:
            return []

        return json.loads(text)


class Automod:
    def __init__(self, cog):
        self.cog = cog
        self.bot = cog.bot
        self.config: list[dict] = load_config()
        self.config_rules: list[dict] = self.config["rules"]
        self.config_guilds: list[int] = self.config["guilds"]
        self.phishing_domains = []
        self.phishing_last_updated = 0
        self.shorteners = ()

    async def check(self, check: str, content: str, member, message=None):
        # skip if guild not configured
        if member.guild.id not in self.config_guilds:
            return

        for rule in self.config_rules:
            _match = False
            rule_type = rule["type"]
            rule_check = rule["check"]

            # skip rules that aren't configured to check the thing we're currently checking
            if check not in rule_check:
                continue

            match rule["type"]:
                case "phishing":
                    _match = await self.check_phishing(content)
                case "words":
                    _match = self.check_word(content, rule)
                case "substring":
                    _match = self.check_substring(content, rule)
                case "regex":
                    _match = self.check_regex(content, rule)
                case _:
                    logger.error(f"Invalid rule type '{rule_type}'")
                    # raise Exception("Invalid rule type.")

            if _match:
                kicked_or_banned = False
                for action in rule["actions"]:
                    match action:
                        case "delete":
                            if message:
                                await message.delete()
                        case "kick":
                            if not kicked_or_banned:
                                kicked_or_banned = True
                                await member.kick()
                        case "ban":
                            if not kicked_or_banned:
                                kicked_or_banned = True
                                await member.ban()

    async def check_message(self, message):
        await self.check("message", message.content, message.author, message)

    async def check_profile(self, member):
        await self.check("profile", member.name, member)
        await self.check("profile", member.global_name, member)
        await self.check("profile", member.nick, member)

    async def pull_phishing_list(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(FISHFISH_API) as resp:
                self.phishing_domains = await resp.json()

    async def pull_shorteners(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(SHORTENERS_URL) as resp:
                self.shorteners = tuple((await resp.read()).split())

    def get_domains(self, content: str) -> str:
        content = content.replace("\u0000", "")  # NUL char handling (temp fix) (TODO)
        content = unquote(content)  # handle urlquoted domains (ugh)
        content = REMOVE_EXTRA_SLASHES.sub(r"\1", content)
        urls = [match.group(0) for match in URL_PATTERN.finditer(content)]

        # domains = set(urlparse(url).netloc for url in urls)
        # bitly link handling (temp fix) (TODO)
        domains = set()
        to_follow = set()
        for url in urls:
            parsed = urlparse(url)
            if parsed.netloc:
                # if parsed.netloc.startswith(self.shorteners):
                #     to_follow.add(url)
                # else:
                domains.add(parsed.netloc)

        if "" in domains:
            domains.remove("")

        return ",".join(domains)

    async def check_phishing(self, content: str) -> bool:
        now = time.time()
        if now - self.phishing_last_updated > 3600:
            await self.pull_phishing_list()
            self.phishing_last_updated = now

        if not self.shorteners:
            await self.pull_shorteners()

        # Runs regex to find URLs and uses urlparse to extract domain for each
        # then rejoins them separated by commas to allow for substring detection.
        # Note: only returns domains of URLs starting with http:// or https://
        domains = self.get_domains(content)

        for phishing_domain in self.phishing_domains:
            if phishing_domain in domains:
                return True

        return False

    def check_word(self, content: str, rule: dict) -> bool:
        for word in rule["match"]:
            if re.search(rf"\b{word}\b", content):
                return True
        return False

    def check_substring(self, content: str, rule: dict) -> bool:
        for substring in rule["match"]:
            if substring in content:
                return True
        return False

    def check_regex(self, content: str, rule: dict) -> bool:
        for pattern in rule["match"]:
            if re.search(pattern, content):
                return True
        return False
