# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from redbot.core import commands
from typing import Optional
from enum import Enum
import numpy as np


class Nation(Enum):
    Aztecs = 0
    Maya = 1
    Inca = 2
    Bantu = 3
    Nubians = 4
    Greeks = 5
    Romans = 6
    Egyptians = 7
    Turks = 8
    Spanish = 9
    French = 10
    British = 11
    Germans = 12
    Russians = 13
    Chinese = 14
    Japanese = 15
    Koreans = 16
    Mongols = 17
    Iroquois = 18
    Lakota = 19
    Americans = 20
    Indians = 21
    Dutch = 22
    Persians = 23

def emojify_color(color: int) -> str:

    if color == 1:
        return "🟥"
    # elif color == 2:
    #     return "🟦"
    elif color == 2:
        return "☑️"
    elif color == 3:
        return "🟪"
    elif color == 4:
        return "🟩"
    elif color == 5:
        return "🟨"
    # elif color == 6:
    #     return "🧊"
    elif color == 6:
        return ":snowflake:"
    elif color == 7:
        return "⬜"
    elif color == 8:
        return "🟧"


def playerify_color(color: int) -> str:

    if color == 1:
        return "P1"
    elif color == 2:
        return "P2"
    elif color == 3:
        return "P3"
    elif color == 4:
        return "P4"
    elif color == 5:
        return "P5"
    elif color == 6:
        return "P6"
    elif color == 7:
        return "P7"
    elif color == 8:
        return "P8"


class RonPicker(commands.Cog):
    """Pick random nations for the game Rise of Nations, using much better randomization."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["pick"])
    async def pick_nations(self, ctx, players: Optional[int] = 8):
        """Pick random nations (duplicates allowed, no spoiler tags)."""
        
        # Generate specified number of random numbers between 0 and 23 inclusive
        random_integers = np.random.randint(low=0, high=24, size=players)

        # Convert to nations and format nicely, with no spoiler tags for each nation
        formatted_nations = [("* `" + playerify_color(i+1) + f":` " + f"{Nation(int_value).name}") for i, int_value in enumerate(random_integers)]
        formatted_nations = "\n".join(formatted_nations)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.darkorange())
        embed.title = "Random nations"
        embed.description = formatted_nations

        #await ctx.send(f"The random nations are:\n{formatted_nations}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["pick2"])
    async def pick_nations_no_repeats(self, ctx, players: Optional[int] = 8):
        """Pick random nations (with no duplicates, no spoiler tags)."""

        # Generate specified number of random numbers between 0 and 23 inclusive, without duplicates
        random_integers = np.random.choice(24, size=players, replace=False)

        # Convert to nations and format nicely, with no spoiler tags for each nation
        formatted_nations = [("* `" + playerify_color(i+1) + f":` " + f"{Nation(int_value).name}") for i, int_value in enumerate(random_integers)]
        formatted_nations = "\n".join(formatted_nations)

                # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.darkorange())
        embed.title = "Random nations"
        embed.description = formatted_nations

        #await ctx.send(f"The random nations are:\n{formatted_nations}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["pick_s"])
    async def pick_nations_spoilers(self, ctx, players: Optional[int] = 8):
        """Pick random nations (duplicates allowed, with spoiler tags)."""
        
        # Generate specified number of random numbers between 0 and 23 inclusive
        random_integers = np.random.randint(low=0, high=24, size=players)

        # Convert to nations and format nicely, with spoiler tags for each nation
        formatted_nations = [("* `" + playerify_color(i+1) + f":` ||`" + f"{Nation(int_value).name:<9}"+ "`||") for i, int_value in enumerate(random_integers)]
        formatted_nations = "\n".join(formatted_nations)

                # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.darkorange())
        embed.title = "Random nations"
        embed.description = formatted_nations

        #await ctx.send(f"The random nations are:\n{formatted_nations}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["pick_s2"])
    async def pick_nations_spoilers_no_repeats(self, ctx, players: Optional[int] = 8):
        """Pick random nations (with no duplicates, with spoiler tags)."""

        # Generate specified number of random numbers between 0 and 23 inclusive, without duplicates
        random_integers = np.random.choice(24, size=players, replace=False)

        # Convert to nations and format nicely, with spoiler tags for each nation
        formatted_nations = [("* `" + playerify_color(i+1) + f":` ||`" + f"{Nation(int_value).name:<9}"+ "`||") for i, int_value in enumerate(random_integers)]
        formatted_nations = "\n".join(formatted_nations)

                # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.darkorange())
        embed.title = "Random nations"
        embed.description = formatted_nations

        #await ctx.send(f"The random nations are:\n{formatted_nations}")
        await ctx.send(embed=embed)