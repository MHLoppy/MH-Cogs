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

class Map(Enum):
    African_Watering_Hole = 0
    Amazon_Rainforest     = 1
    Australian_Outback    = 2
    Great_Lakes           = 3
    Great_Sahara          = 4
    Himalayas             = 5
    Old_World             = 6
    Southwest_Mesa        = 7
    Mediterranean         = 8   # BEGIN SEA MAPS
    Atlantic_Sea_Power    = 9
    British_Isles         = 10
    Colonial_Powers       = 11
    East_Indies           = 12
    East_Meets_West       = 13
    New_World             = 14
    Nile_Delta            = 15
    Warring_States        = 16

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
        player = await self.playerify_color(count)
        return "* `" + player + f":` " + f"{Nation(nation_int).name}"

    async def format_pick_spoilers(self, count: int, nation_int: int) -> str:
        player = await self.playerify_color(count)
        return "* `" + player + f":` ||`" + f"{Nation(nation_int).name:<9}"+ "`||"# <9 is part of the padding to make the output length uniform

    async def format_map(self, count: int, map_int: int) -> str:
        map_str = "Map " + str(count)
        msg = "* `" + map_str + f":` " + f"{Map(map_int).name}"
        msg = msg.replace("_", " ")
        return msg

    @commands.command(aliases=["pick"])
    async def pick_nations(self, ctx, players: Optional[int] = 8, *, desc: Optional[str] = None):
        """Pick random nations (duplicates allowed, no spoiler tags)."""
        
        if players < 1 or players > 8:
            await ctx.send("Player count is limited to 1-8.")
            return
        
        if desc and len(desc) > 100:
            await ctx.send("Description too long (max 100 characters).")
            return
        
        # Generate specified number of random numbers between 0 and 23 inclusive
        random_integers = self.rng.integers(low=0, high=24, size=players)

        # Convert to nations and format nicely, with no spoiler tags for each nation
        formatted_nations = [(await self.format_pick(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_nations = "\n".join(formatted_nations)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.dark_orange())
        embed.title = "Random nation"
        if players == 1:
            embed.title = embed.title + "s"
        embed.description = formatted_nations
        embed.set_footer(text="Duplicate nations allowed")
        if desc:
            embed.title = embed.title + " for " + desc
            embed.colour=discord.Colour.dark_gold()

        await ctx.send(embed=embed)

    @commands.command(aliases=["pick2", "picku"])
    async def pick_nations_no_repeats(self, ctx, players: Optional[int] = 8, *, desc: Optional[str] = None):
        """Pick random nations (with no duplicates, no spoiler tags)."""

        if players < 1 or players > 8:
            await ctx.send("Player count is limited to 1-8.")
            return
        
        if desc and len(desc) > 100:
            await ctx.send("Description too long (max 100 characters).")
            return

        # Generate specified number of random numbers between 0 and 23 inclusive, without duplicates
        random_integers = self.rng.choice(24, size=players, replace=False)

        # Convert to nations and format nicely, with no spoiler tags for each nation
        formatted_nations = [(await self.format_pick(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_nations = "\n".join(formatted_nations)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.dark_orange())
        embed.title = "Random nation"
        if players == 1:
            embed.title = embed.title + "s"
        embed.description = formatted_nations
        embed.set_footer(text="Duplicate nations not allowed")
        if desc:
            embed.title = embed.title + " for " + desc
            embed.colour=discord.Colour.dark_gold()

        await ctx.send(embed=embed)

    @commands.command(aliases=["pick_s"])
    async def pick_nations_spoilers(self, ctx, players: Optional[int] = 8, *, desc: Optional[str] = None):
        """Pick random nations (duplicates allowed, with spoiler tags)."""
        
        if players < 1 or players > 8:
            await ctx.send("Player count is limited to 1-8.")
            return
        
        if desc and len(desc) > 100:
            await ctx.send("Description too long (max 100 characters).")
            return
        
        # Generate specified number of random numbers between 0 and 23 inclusive
        random_integers = self.rng.integers(low=0, high=24, size=players)

        # Convert to nations and format nicely, with spoiler tags for each nation
        formatted_nations = [(await self.format_pick_spoilers(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_nations = "\n".join(formatted_nations)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.dark_orange())
        embed.title = "Random nation"
        if players == 1:
            embed.title = embed.title + "s"
        embed.description = formatted_nations
        embed.set_footer(text="Duplicate nations allowed")
        if desc:
            embed.title = embed.title + " for " + desc
            embed.colour=discord.Colour.dark_gold()

        await ctx.send(embed=embed)

    @commands.command(aliases=["pick_s2", "picku_s"])
    async def pick_nations_spoilers_no_repeats(self, ctx, players: Optional[int] = 8, *, desc: Optional[str] = None):
        """Pick random nations (with no duplicates, with spoiler tags)."""

        if players < 1 or players > 8:
            await ctx.send("Player count is limited to 1-8.")
            return
        
        if desc and len(desc) > 100:
            await ctx.send("Description too long (max 100 characters).")
            return

        # Generate specified number of random numbers between 0 and 23 inclusive, without duplicates
        random_integers = self.rng.choice(24, size=players, replace=False)

        # Convert to nations and format nicely, with spoiler tags for each nation
        formatted_nations = [(await self.format_pick_spoilers(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_nations = "\n".join(formatted_nations)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.dark_orange())
        embed.title = "Random nation"
        if players == 1:
            embed.title = embed.title + "s"
        embed.description = formatted_nations
        embed.set_footer(text="Duplicate nations not allowed")
        if desc:
            embed.title = title + " for " + desc
            embed.colour=discord.Colour.dark_gold()

        await ctx.send(embed=embed)
    
    # An interesting adaptation would be to run the output on a custom server with map emoji, then forward the message to the server it was called from
    @commands.command(aliases=["map"])
    async def pick_map(self, ctx, pool_size: Optional[int] = 1, *, desc: Optional[str] = None):
        """Pick a specified number of random maps (duplicates allowed)."""
        
        if pool_size < 1 or pool_size > 9:
            await ctx.send("Map count is limited to 1-9.")
            return
        
        if desc and len(desc) > 100:
            await ctx.send("Description too long (max 100 characters).")
            return

        # Generate specified number of random numbers between 0 and 16 inclusive
        random_integers = self.rng.integers(low=0, high=17, size=pool_size)

        # Convert to maps and format nicely
        formatted_maps = [(await self.format_map(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_maps = "\n".join(formatted_maps)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.gold())
        embed.title = "Random map"
        if pool_size == 1:
            embed.title = embed.title + "s"
        embed.description = formatted_maps
        embed.set_footer(text="Duplicate maps allowed")
        if desc:
            embed.title = title + " for " + desc

        await ctx.send(embed=embed)
    
    @commands.command(aliases=["mapu"])
    async def pick_map_no_duplicates(self, ctx, pool_size: Optional[int] = 1, *, desc: Optional[str] = None):
        """Pick a specified number of random maps (duplicates not allowed)."""
        
        if pool_size < 1 or pool_size > 9:
            await ctx.send("Map count is limited to 1-9.")
            return
        
        if desc and len(desc) > 100:
            await ctx.send("Description too long (max 100 characters).")
            return

        # Generate specified number of random numbers between 0 and 16 inclusive
        random_integers = self.rng.choice(17, size=pool_size, replace=False)

        # Convert to maps and format nicely
        formatted_maps = [(await self.format_map(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_maps = "\n".join(formatted_maps)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.gold())
        embed.title = "Random map"
        if pool_size == 1:
            embed.title = embed.title + "s"
        embed.description = formatted_maps
        embed.set_footer(text="Duplicate maps not allowed")
        if desc:
            embed.title = title + " for " + desc

        await ctx.send(embed=embed)
    
    @commands.command(aliases=["lmap", "landmap"])
    async def pick_map_land(self, ctx, pool_size: Optional[int] = 1, *, desc: Optional[str] = None):
        """Pick a specified number of random land maps (duplicates allowed)."""
        
        if pool_size < 1 or pool_size > 9:
            await ctx.send("Map count is limited to 1-9.")
            return
        
        if desc and len(desc) > 100:
            await ctx.send("Description too long (max 100 characters).")
            return

        # Generate specified number of random numbers between 0 and 7 inclusive
        random_integers = self.rng.integers(low=0, high=8, size=pool_size)

        # Convert to maps and format nicely
        formatted_maps = [(await self.format_map(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_maps = "\n".join(formatted_maps)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.green())
        embed.title = "Random land map"
        if pool_size == 1:
            embed.title = embed.title + "s"
        embed.description = formatted_maps
        embed.set_footer(text="Duplicate maps allowed")
        if desc:
            embed.title = title + " for " + desc

        await ctx.send(embed=embed)
    
    @commands.command(aliases=["lmapu", "landmapu"])
    async def pick_map_no_duplicates(self, ctx, pool_size: Optional[int] = 1, *, desc: Optional[str] = None):
        """Pick a specified number of random land maps (duplicates not allowed)."""
        
        if pool_size < 1 or pool_size > 9:
            await ctx.send("Map count is limited to 1-9.")
            return
        
        if desc and len(desc) > 100:
            await ctx.send("Description too long (max 100 characters).")
            return

        # Generate specified number of random numbers between 0 and 16 inclusive
        random_integers = self.rng.choice(8, size=pool_size, replace=False)

        # Convert to maps and format nicely
        formatted_maps = [(await self.format_map(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_maps = "\n".join(formatted_maps)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.green())
        embed.title = "Random land map"
        if pool_size == 1:
            embed.title = embed.title + "s"
        embed.description = formatted_maps
        embed.set_footer(text="Duplicate maps not allowed")
        if desc:
            embed.title = title + " for " + desc

        await ctx.send(embed=embed)
    
    @commands.command(aliases=["smap", "seamap", "wmap"])
    async def pick_map_sea(self, ctx, pool_size: Optional[int] = 1, *, desc: Optional[str] = None):
        """Pick a specified number of random sea maps (duplicates allowed)."""
        
        if pool_size < 1 or pool_size > 9:
            await ctx.send("Map count is limited to 1-9.")
            return
        
        if desc and len(desc) > 100:
            await ctx.send("Description too long (max 100 characters).")
            return

        # Generate specified number of random numbers between 9 and 16 inclusive
        random_integers = self.rng.integers(low=9, high=17, size=pool_size)

        # Convert to maps and format nicely
        formatted_maps = [(await self.format_map(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_maps = "\n".join(formatted_maps)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.title = "Random sea map"
        if pool_size == 1:
            embed.title = embed.title + "s"
        embed.description = formatted_maps
        embed.set_footer(text="Duplicate maps allowed")
        if desc:
            embed.title = title + " for " + desc

        await ctx.send(embed=embed)
    
    @commands.command(aliases=["smapu", "seamapu", "wmapu"])
    async def pick_map_sea_no_duplicates(self, ctx, pool_size: Optional[int] = 1, *, desc: Optional[str] = None):
        """Pick a specified number of random sea maps (duplicates not allowed)."""
        
        if pool_size < 1 or pool_size > 9:
            await ctx.send("Map count is limited to 1-9.")
            return
        
        if desc and len(desc) > 100:
            await ctx.send("Description too long (max 100 characters).")
            return

        # Generate specified number of random numbers between 9 and 16 inclusive
        random_integers = self.rng.choice(np.arange(9, 17), size=pool_size, replace=False)

        # Convert to maps and format nicely
        formatted_maps = [(await self.format_map(i+1, int_value)) for i, int_value in enumerate(random_integers)]
        formatted_maps = "\n".join(formatted_maps)

        # Construct and send an embed message
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.title = "Random sea map"
        if pool_size == 1:
            embed.title = embed.title + "s"
        embed.description = formatted_maps
        embed.set_footer(text="Duplicate maps not allowed")
        if desc:
            embed.title = title + " for " + desc

        await ctx.send(embed=embed)