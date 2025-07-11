# MH-Cogs
Cogs (plugins) for [Red](https://github.com/Cog-Creators/Red-DiscordBot), a Discord bot. Cogs are for Red v3 unless stated otherwise.

## Cog list
| Cog | Description |
|---|---|
| autopost_v3 | <details><summary>Automatically posts daily weather forecasts, and displays weather summary on-command for a given location.</summary> Primary commands: `[p]autopost` and `[p]weathershort` (alias `[p]ws`). ![Example of weathershort, using the "ws" command alias.](https://i.imgur.com/3Rrmxaa.png).</details> |
| ronrobtaunts | <details><summary>Automatically responds to messages with corresponding Rise of Babel taunts (from Rise of Nations).</summary>Very simple cog, made in a couple of hours. Does not convert or remove #ICON text. ![Example of RoB taunts 138 and 879.](https://i.imgur.com/jxUm630.png).</details> |
| ronpicker | <details><summary>Picks random nations or maps for Rise of Nations, since the game's built-in RNG is bad.</summary> Commands: `[p]pick` and `[p]pick_s` allow dupes, `[p]pick2` and `[p]pick_s2` don't. Player count defaults to 8. ![Example of pick.](https://i.imgur.com/jXJji52.png).</details> |

## Credits
* autopost_v3 is based on [TrustyJAID's weather cog](https://github.com/TrustyJAID/Trusty-cogs) and draws from my own [v2 version of the autopost cog](https://github.com/MHLoppy/Autopost-v2), which itself is based on a previous weather cog by rfilkins1992 & Will. Some of the API calls made rely on the API key from TrustyJAID's cog!
* ronrobtaunts is based on [Falcom's hiback cog](https://github.com/nmbook/FalcomBot-cogs), and obviously uses the [Rise of Babel taunt list from 2005](https://web.archive.org/web/20120502125628/http://mastersleague.net/Downloads/details/id=1.html) compiled by Fedomar of the Fish Sticks Foundation (the dead link on taunt 879 has been updated).
* ronpicker's space-padding on its spoiler-tagged responses was aided by [Justin Furuness (and others)](https://stackoverflow.com/a/62617715/16367940).
