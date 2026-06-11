"""
technically-automod
"""

###################
# IMPORT ATTEMPTS #
###################

try:
    import discord as _discordpy
except ModuleNotFoundError:
    _discordpy = None

try:
    import disnake as _disnake
except ModuleNotFoundError:
    _disnake = None

try:
    import nextcord as _nextcord
except ModuleNotFoundError:
    _nextcord = None

##################################
# CONDITIONALLY IMPORTED MODULES #
##################################

if _discordpy:
    import cog_discordpy
    from cog_discordpy import DiscordpyAutomodCog

if _disnake:
    import cog_disnake
    from cog_disnake import DisnakeAutomodCog

if _nextcord:
    import cog_nextcord
    from cog_nextcord import NextcordAutomodCog

############################################################
# ERROR BEHAVIOR IF WE CAN'T AUTOMATICALLY CHOOSE A MODULE #
############################################################

_error_message = (
    "Found multiple Discord API libraries. Please explicitly import "
    "DiscordpyAutomodCog, DisnakeAutomodCog, or NextcordAutomodCog; "
    "OR use technically_automod.cog_discordpy, technically_automod.cog_disnake, or technically_automod.cog_nextcord "
    "when calling load_extension."
)

class _BadCog:
    def __init__(self, _):
        raise ImportError(_error_message)

def bad_setup(_):
    raise ImportError(_error_message)

####################################################
# AUTOMATICALLY SET COG BASED ON AVAILABLE MODULES #
####################################################

lib = None
libname = None
TechnicallyAutomodCog: "DiscordpyAutomodCog | DisnakeAutomodCog | NextcordAutomodCog | _BadCog" = _BadCog

if _discordpy:
    if not (_disnake or _nextcord):
        lib = _discordpy
        libname = "discordpy"
        TechnicallyAutomodCog = DiscordpyAutomodCog
        setup = cog_discordpy.setup
    else:
        lib = None
        libname = None
        TechnicallyAutomodCog = _BadCog
        setup = bad_setup

if _disnake:
    if not (_discordpy or _nextcord):
        lib = _disnake
        libname = "disnake"
        TechnicallyAutomodCog = DisnakeAutomodCog
        setup = cog_disnake.setup
    else:
        lib = None
        libname = None
        TechnicallyAutomodCog = _BadCog
        setup = bad_setup

if _nextcord:
    if not (_discordpy or _disnake):
        lib = _nextcord
        libname = "nextcord"
        TechnicallyAutomodCog = NextcordAutomodCog
        setup = cog_nextcord.setup
    else:
        lib = None
        libname = None
        TechnicallyAutomodCog = _BadCog
        setup = bad_setup

if lib is None:
    raise ImportError("No Discord API library found.")