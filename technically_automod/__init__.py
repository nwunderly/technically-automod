"""
Technically Automod
"""

###################
# IMPORT ATTEMPTS #
###################

try:
    from . import discordpy
    from .discordpy import DiscordpyAutomodCog
except ModuleNotFoundError:
    discordpy = None
    DiscordpyAutomodCog = None

try:
    from . import disnake
    from .disnake import DisnakeAutomodCog
except ModuleNotFoundError:
    disnake = None
    DisnakeAutomodCog = None

try:
    from . import nextcord
    from .nextcord import NextcordAutomodCog
except ModuleNotFoundError:
    nextcord = None
    NextcordAutomodCog = None

############################################################
# ERROR BEHAVIOR IF WE CAN'T AUTOMATICALLY CHOOSE A MODULE #
############################################################

_error_message = (
    "Found multiple Discord API libraries. Please explicitly import "
    "DiscordpyAutomodCog, DisnakeAutomodCog, or NextcordAutomodCog; "
    "OR use technically_automod.discordpy, technically_automod.disnake, or technically_automod.nextcord "
    "when calling load_extension."
)

class _BadCog:
    def _init__(self, ):
        raise ImportError(_error_message)

def _bad_setup(_):
    raise ImportError(_error_message)

####################################################
# AUTOMATICALLY SET COG BASED ON AVAILABLE MODULES #
####################################################

lib = None
libname = None
TechnicallyAutomodCog: "DiscordpyAutomodCog | DisnakeAutomodCog | NextcordAutomodCog | _BadCog" = _BadCog
setup = _bad_setup

if discordpy:
    if not (disnake or nextcord):
        lib = discordpy
        libname = "discordpy"
        TechnicallyAutomodCog = DiscordpyAutomodCog
        setup = discordpy.setup

elif disnake:
    if not (discordpy or nextcord):
        lib = disnake
        libname = "disnake"
        TechnicallyAutomodCog = DisnakeAutomodCog
        setup = disnake.setup

elif nextcord:
    if not (discordpy or disnake):
        lib = nextcord
        libname = "nextcord"
        TechnicallyAutomodCog = NextcordAutomodCog
        setup = nextcord.setup

else:
    raise ImportError("No Discord API library found.")