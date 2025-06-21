# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import discord
import numpy as np

from enum import Enum
from redbot.core import commands
from typing import Optional


class Nation(Enum):
    Aztecs    = 0
    Maya      = 1
    Inca      = 2
    Bantu     = 3
    Nubians   = 4
    Greeks    = 5
    Romans    = 6
    Egyptians = 7
    Turks     = 8
    Spanish   = 9
    French    = 10
    British   = 11
    Germans   = 12
    Russians  = 13
    Chinese   = 14
    Japanese  = 15
    Koreans   = 16
    Mongols   = 17
    Iroquois  = 18
    Lakota    = 19
    Americans = 20
    Indians   = 21
    Dutch     = 22
    Persians  = 23

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
    else:
        return "❌"


class RonPicker(commands.Cog):
    """Pick random nations for the game Rise of Nations, using much better randomization."""

    def __init__(self, bot):
        self.bot = bot
        self.rng_engine = np.random.PCG64DXSM()
        self.rng = np.random.Generator(self.rng_engine)

    async def playerify_color(self, color: int) -> str:
        return "P" + str(color)

    async def format_pick(self, count: int, nation_int: int) -> str:
        return "* `" + self.playerify_color(count) + f":` " + f"{Nation(nation_int).name}"

    async def format_pick_spoilers(self, count: int, nation_int: int) -> str:
        return "* `" + self.playerify_color(count) + f":` ||`" + f"{Nation(nation_int).name:<9}"+ "`||"# <9 is part of the padding to make the output length uniform

    @commands.command(aliases=["pick"])
    async def pick_nations(self, ctx, players: Optional[int] = 8):
        """Pick random nations (duplicates allowed, no spoiler tags)."""
        
        if players < 1 or players > 8:
            await ctx.send("Player count is limited to 1-8.")
            return
        
        # Generate specified number of random numbers between 0 and 23 inclusive
        random_integers = self.rng.integers(low=0, high=24, size=players)

        # Convert to nations and format nicely, with no spoiler tags for each nation
        formatted_nations = [(await self.format_pick(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_nations = "\n".join(formatted_nations)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.dark_orange())
        embed.title = "Random nations"
        embed.description = formatted_nations

        #await ctx.send(f"The random nations are:\n{formatted_nations}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["pick2", "picku"])
    async def pick_nations_no_repeats(self, ctx, players: Optional[int] = 8):
        """Pick random nations (with no duplicates, no spoiler tags)."""

        if players < 1 or players > 8:
            await ctx.send("Player count is limited to 1-8.")
            return

        # Generate specified number of random numbers between 0 and 23 inclusive, without duplicates
        random_integers = self.rng.choice(24, size=players, replace=False)

        # Convert to nations and format nicely, with no spoiler tags for each nation
        formatted_nations = [(await self.format_pick(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_nations = "\n".join(formatted_nations)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.dark_orange())
        embed.title = "Random nations (no duplicates)"
        embed.description = formatted_nations

        #await ctx.send(f"The random nations are:\n{formatted_nations}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["pick_s"])
    async def pick_nations_spoilers(self, ctx, players: Optional[int] = 8):
        """Pick random nations (duplicates allowed, with spoiler tags)."""
        
        if players < 1 or players > 8:
            await ctx.send("Player count is limited to 1-8.")
            return
        
        # Generate specified number of random numbers between 0 and 23 inclusive
        random_integers = self.rng.integers(low=0, high=24, size=players)

        # Convert to nations and format nicely, with spoiler tags for each nation
        formatted_nations = [(await self.format_pick_spoilers(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_nations = "\n".join(formatted_nations)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.dark_orange())
        embed.title = "Random nations"
        embed.description = formatted_nations

        #await ctx.send(f"The random nations are:\n{formatted_nations}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["pick_s2", "picku_s"])
    async def pick_nations_spoilers_no_repeats(self, ctx, players: Optional[int] = 8):
        """Pick random nations (with no duplicates, with spoiler tags)."""

        if players < 1 or players > 8:
            await ctx.send("Player count is limited to 1-8.")
            return

        # Generate specified number of random numbers between 0 and 23 inclusive, without duplicates
        random_integers = self.rng.choice(24, size=players, replace=False)

        # Convert to nations and format nicely, with spoiler tags for each nation
        formatted_nations = [(await self.format_pick_spoilers(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_nations = "\n".join(formatted_nations)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.dark_orange())
        embed.title = "Random nations (no duplicates)"
        embed.description = formatted_nations

        #await ctx.send(f"The random nations are:\n{formatted_nations}")
        await ctx.send(embed=embed)