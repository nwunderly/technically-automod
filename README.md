# Technically Automod
Privileged intent justification for Python-based discord bots.

technically-automod is an automod cog for major Python-based Discord API frameworks (Discord.py, Disnake, Nextcord).


## Installing

technically-automod can be installed with the command

```sh
# Linux
python3 -m pip install -U technically-automod

# Windows
python -m pip install -U technically-automod
```

To install the development version of the library directly from source:

```sh
$ git clone https://github.com/nwunderly/technically-automod
$ cd technically-automod
$ python3 -m pip install -U .
```

To ensure version compatibility with your Discord API library:

```sh
# discord.py
pip install technically-automod[discord.py]

# disnake
pip install technically-automod[disnake]

# nextcord
pip install technically-automod[nextcord]
```


## Loading the extension

You can load technically-automod the same way you load any other extension. The library will automatically detect
which Discord API library you have installed, and choose the correct extension to load.

```py
# discord.py
await bot.load_extension("technically_automod")

# disnake & nextcord
bot.load_extension("technically_automod")
```

If you have multiple Discord API libraries installed, the above method will raise an ImportError exception.
If this happens, you should load the extension based on the library you're using:

```py
# discord.py
await bot.load_extension("technically_automod.discordpy")

# disnake
bot.load_extension("technically_automod.disnake")

# nextcord
bot.load_extension("technically_automod.nextcord")
```

You can also add the Cog manually:

```py
# Auto-detect library
from technically_automod import TechnicallyAutomodCog
await bot.add_cog(TechnicallyAutomodCog(bot)) # if using discord.py
bot.add_cog(TechnicallyAutomodCog(bot)) # if using disnake or nextcord

# discord.py
from technically_automod import DiscordpyAutomodCog
await bot.add_cog(DiscordpyAutomodCog(bot))

# disnake
from technically_automod import DisnakeAutomodCog
bot.add_cog(DisnakeAutomodCog(bot))

# nextcord
from technically_automod import NextcordAutomodCog
bot.add_cog(NextcordAutomodCog(bot))
```


## Configuration

When loaded, the automod cog will look for a file called "config.json" in the Python process's working directory.
An example config file is provided in this repository.

The config should be structured as a JSON object with two fields:

- `guilds` should be a list of guild IDs to do automoderation in.
- `rules` should be a list of rules, where each rule consists of a name, a rule type, actions to perform on match,
and (if necessary) a list of items to match on.

### Disable Automod

Automod will do nothing if:

1. There is no `config.json` file.
2. `config.json` is empty.
3. The `guilds` field is missing, or contains an empty list: `[]`
3. The `rules` field is missing, or contains an empty list: `[]`

### Rule Types

The `type` field should be a string defining the rule type.

1. Rule type `phishing` will use the [FishFish](https://fishfish.gg) database to detect phishing links.
   The cog will update the phishing domain list every hour if the configuration contains a phishing rule.
2. Rule type `words` will match whole words in the message content.
3. Rule type `substring` will detect the matches anywhere in the message content, including in the middle of words.
4. Rule type `regex` will use Python's `re.search` function to find regex pattern matches in the message content.

Note: `words`, `substring`, and `regex` rules are all case-insensitive when matching.

### Check

The `check` field should be a list of strings indicating what the rule should apply to.

1. If `message` is in the list, the rule will be used to check the content of messages.
   This requires the `message_content` intent.
2. If `profile` is in the list, the rule will be used to check member username, global display name, and nickname.
   This requires the `members` intent.

Note: you can find more info on privileged intents [here](https://docs.discord.com/developers/events/gateway#privileged-intents).

### Match List

The `match` field in each rule should be a list of strings defining the words, substrings,
or regex patterns to match on. The `phishing` rule should not have a `match` field.

### Actions

The `actions` field should be a list of actions to perform if a match is detected. The options are:

1. `delete` - Delete the message.
2. `kick` - Kick the user from the server.
3. `ban` - Ban the user from the server.

Note: if "kick" and "ban" are both listed, the one listed first will be performed and the next will be ignored.

### Examples

Example `config.json` file:

```json
{
  "guilds": [],
  "rules": [
    {
      "name": "Phishing Detection",
      "type": "phishing",
      "check": ["message"],
      "actions": ["delete", "kick"]
    },
    {
      "name": "Bad Word Detection",
      "type": "words",
      "check": ["message", "profile"],
      "match": ["heck", "frick"],
      "actions": ["delete", "kick"]
    },
    {
      "name": "Brainrot Detecton",
      "type": "substring",
      "check": ["message"],
      "match": ["67"],
      "actions": []
    },
    {
      "name": "Spam Detection",
      "type": "regex",
      "check": ["message"],
      "match": ["(?:\w+){30,}"],
      "actions": ["delete"]
    }
  ]
}
```


## Justifying Privileged Intents

This automod cog supports automatic moderation of message content (this requires the Message Content privileged intent)
and members' usernames, display names, and nicknames (this requires the Guild Members privileged intent).

The cog supports several things not available in stock Discord automod:
- Detection of phishing links using the FishFish API.
- Regex rules use the Python `re` module, which supports lookaheads and lookbehinds, something that Discord's native automod
  does not support.

I believe the functionality provided by this library should be sufficient justification to get a bot approved for access to
either, or both, of those intents.


## Why?

While this library is completely functional, I created it more as a form of protest than out of a desire to undermine or skirt around Discord's rules. It's a pretty barebones and limited automod cog, but it also contains the functionality required to justify approval for the Message Content and Guild Members intents.

On June 10, 2026, Discord announced a [change to their Privileged Intents system](https://support-dev.discord.com/hc/en-us/articles/40281523410967-Changes-to-Privileged-Intent-Access-for-Discord-Apps): apps accessible to more than 10,000 users now have to apply and be approved for access to privileged intents. There is a 90-day deadline to apply. If Discord doesn't consider your use case for privileged intents to be valid (for example, message commands), this means you have 90 days (plus however long it takes Discord to review), to update your bot to make it work without access to privileged intents.

Previously, bots that had been added to more than 100 servers would have to be approved for access to these intents. This makes sense, as there are bots that are in *millions* of servers, with access to *tens of millions* of users. These applications, often owned by businesses whose sole purpose is to run these services for profit, should be scrutinized to ensure that they are not abusing the data of their users. When Discord bots are added to hundreds, thousands, or millions of servers, they are effectively public web services.

**This change adjusts the requirement to also include bespoke, private bots created for large communities.** The custom moderation bot in a single server with 10,000 people is *not* the same threat to user data that a large, public bot is.

With this change, Discord is stating that message commands are not acceptable for large communities' custom bots. Such bots, if they don't have another "valid" use case for message content, *must* move to slash commands or they will cease to function in September.

As an admin of a large community on Discord, my team and I rely heavily on custom bots to help us with moderation. We also have
several bots that exist solely to help create a fun environment in our community. In total, we have **NINE** bots (owned by two people) that exist solely for this single community. That's nine bots we have to figure out how to justify, or rewrite, with only a few months' notice. That's a huge lift for a handful of people, all of whom have day jobs.

This change forces a large amount of completely unnecessary bureaucratic nonsense on the moderation teams of large communities, as well as forcing them to rewrite custom bots on short notice or lose the software they depend on to help keep their communities safe and enjoyable. Bots that *nearly every* large community has, because Discord's built-in moderation tools are not sufficient for the needs of these large communities.

**I created this library because I strongly believe that Discord has no business policing the tools that moderation teams create to help them run their communities in this way. Discord should be making it easier to manage large communities, not more difficult.**
