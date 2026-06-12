# Technically Automod
Message intent justification for Python-based discord bots.

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

The config should be structured as a list of rules, where each rule consists of a name, a rule type, actions to perform on match,
and (if necessary) a list of items to match on.

### Disable Automod

Automod will do nothing if:

1. There is no `config.json` file.
2. `config.json` is empty.
3. `config.json` contains an empty json list: `[]`

### Rule Types

The `type` field should be a string defining the rule type.

1. Rule type `phishing` will use the [FishFish](https://fishfish.gg) database to detect phishing links.
   The extension will update the phishing domain list every hour if the configuration contains a phishing rule.
2. Rule type `words` will match whole words in the message content.
3. Rule type `substring` will detect the matches anywhere in the message content, including in the middle of words.
4. Rule type `regex` will use Python's `re.search` function to find regex pattern matches in the message content.

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
[
  {
    "name": "Phishing Detection",
    "type": "phishing",
    "actions": ["delete", "kick"]
  },
  {
    "name": "Bad Word Detection",
    "type": "words",
    "match": ["heck", "frick"],
    "actions": ["delete"]
  },
  {
    "name": "Brainrot Detecton",
    "type": "substring",
    "match": ["67"],
    "actions": []
  },
  {
    "name": "Spam Detection",
    "type": "regex",
    "match": ["(?:\w+){30,}"],
    "actions": ["delete"]
  }
]
```