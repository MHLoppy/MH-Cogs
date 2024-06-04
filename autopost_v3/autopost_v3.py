# autopost v3 cog by MHLoppy
# (based on weather cog by TrustyJAID, and using their OpenWeather API key!)

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime, timedelta
from typing import Literal, Optional
from urllib.parse import urlencode

import aiohttp
import discord
import asyncio
from discord.ext.commands.converter import Converter
from discord.ext.commands.errors import BadArgument
from redbot.core import Config, checks, commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Autopost", __file__)


class UnitConverter(Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> Optional[str]:
        new_units = None
        if argument.lower() in ["f", "imperial", "mph"]:
            new_units = "imperial"
        elif argument.lower() in ["c", "metric", "kph"]:
            new_units = "metric"
        elif argument.lower() in ["clear", "none"]:
            new_units = None
        else:
            raise BadArgument(_("`{units}` is not a vaild option!").format(units=argument))
        return new_units


@cog_i18n(_)
class Autopost(commands.Cog):
    """Posts weather from https://openweathermap.org"""

    __author__ = ["MHLoppy"]
    __version__ = "3.4.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 354298042)#replaced unique ID with a new randomly generated value from random.org
        default = {"units": None}
        default_guild = {
            "autopostlocation": "",
            "autopostchannel": "",
            "autoposttime": "",
            "autopoststate": False#gura I used to store these bools as strings LET'S GOOOOOOOOOOOOOOOOOOO
        }
        self.config.register_global(**default)
        self.config.register_guild(**default, **default_guild)
        self.config.register_user(**default)
        self.unit = {
            "imperial": {"code": ["i", "f"], "speed": "mph", "temp": " °F"},
            "metric": {"code": ["m", "c"], "speed": "km/h", "temp": " °C"},
        }

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ):
        """
        Method for finding users data inside the cog and deleting it.
        """
        await self.config.user_from_id(user_id).clear()

    @commands.group(name="autopost", invoke_without_command=True)
    @checks.mod_or_permissions(manage_messages=True)
    @commands.bot_has_permissions(embed_links=True)
    async def autopost(self, ctx: commands.Context) -> None:
        """
        When configured, posts weather forecast data for a specified city every 24 hours.
        """
        await self.autopost_loop(ctx)

    # @commands.group(name="weathershort", aliases=["ws", "we2"], invoke_without_command=True)
    # @commands.bot_has_permissions(embed_links=True)
    # async def weathershort(self, ctx: commands.Context, *, location: str) -> None:
        # """
        # Show weather forecast (not current weather!) for a given location.

        # `location` must take the form of `city, Country Code`
        # example: `[p]weathershort New York,US`
        # """
        # await ctx.typing()
        # await self.get_weathershort(ctx, location=location)

    # @weathershort.command(name="zip")
    # @commands.bot_has_permissions(embed_links=True)
    # async def weathershort_by_zip(self, ctx: commands.Context, *, zipcode: str) -> None:
        # """
        # Show weather forecast (not current weather!) for a given location.

        # `zipcode` must be a valid ZIP code or `ZIP code, Country Code` (assumes US otherwise)
        # example: `[p]weathershort zip 20500`
        # """
        # await ctx.typing()
        # await self.get_weathershort(ctx, zipcode=zipcode)

    # @weathershort.command(name="cityid")
    # @commands.bot_has_permissions(embed_links=True)
    # async def weathershort_by_cityid(self, ctx: commands.Context, *, cityid: int) -> None:
        # """
        # Show weather forecast (not current weather!) for a given location.

        # `cityid` must be a valid openweathermap city ID
        # (get list here: <https://bulk.openweathermap.org/sample/city.list.json.gz>)
        # example: `[p]weathershort cityid 2172797`
        # """
        # await ctx.typing()
        # await self.get_weathershort(ctx, cityid=cityid)

    @commands.group(name="weather_forecast", aliases=["wf"], invoke_without_command=True)
    @commands.bot_has_permissions(embed_links=True)
    async def weather_forecast(self, ctx: commands.Context, *, location: str) -> None:
        """
        Show a next-day weather forecast for a given location.

        `location` must take the form of `city, Country Code`
        example: `[p]weathershort New York,US`
        """
        await ctx.typing()
        await self.get_weather_forecast(ctx, location=location)

    @commands.group(name="weather_current", aliases=["wc"], invoke_without_command=True)
    @commands.bot_has_permissions(embed_links=True)
    async def weather_current(self, ctx: commands.Context, *, location: str) -> None:
        """
        Show current weather for a given location.

        `location` must take the form of `city, Country Code`
        example: `[p]weathershort New York,US`
        """
        await ctx.typing()
        await self.get_weather_current(ctx, location=location)

    @commands.group(name="autopostset")
    async def autopost_set(self, ctx: commands.Context) -> None:
        """Set cog settings, such as user or guild default units, or autopost channel."""
        pass

    @autopost_set.command(name="guild", aliases=["server"])
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def set_guild(self, ctx: commands.Context, units: UnitConverter) -> None:
        """
        Sets the guild default weather units.

        `units` must be metric or imperial
        """
        guild = ctx.message.guild
        await self.config.guild(guild).units.set(units)
        await ctx.send(_("Server's default units set to `{units}`").format(units=str(units)))

    @autopost_set.command(name="bot")
    @checks.mod_or_permissions(manage_messages=True)
    async def set_bot(self, ctx: commands.Context, units: UnitConverter) -> None:
        """
        Sets the bots default weather units.

        `units` must be metric or imperial
        """
        await self.config.units.set(units)
        await ctx.send(_("Bots default units set to {units}").format(units=str(units)))

    @autopost_set.command(name="user")
    async def set_user(self, ctx: commands.Context, units: UnitConverter) -> None:
        """
        Sets the user default weather units.

        `units` must be metric or imperial
        Note: User settings override guild settings.
        """
        author = ctx.message.author
        await self.config.user(author).units.set(units)
        await ctx.send(
            _("{author} default units set to `{units}`").format(
                author=author.display_name, units=str(units)
            )
        )

    @autopost_set.command(name="time")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def set_time(self, ctx: commands.Context, *, time: int) -> None:
        """
        Sets the time (Unix time, seconds) to begin autoposting (if not set, time of command is used).
        
        example: `[p]autopostset time 1737810025`
        """
        guild = ctx.message.guild
        if time < (datetime.now().timestamp() - 86400):
            await ctx.send("Time cannot be set earlier than 24 hours ago.")
            return
        else:
            await self.config.guild(guild).autoposttime.set(str(time))
            await ctx.send("Autoposting time set to " + "<t:" + str(time) + ">.")

    @autopost_set.command(name="channel")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def set_channel(self, ctx: commands.Context, *, channel: int) -> None:
        """
        Sets the channel to autopost in (if not set, uses channel where autopost command is sent).
        
        example: `[p]autopostset channel 474088964676911124`
        """
        guild = ctx.message.guild
        await self.config.guild(guild).autopostchannel.set(str(channel))
        await ctx.send(_("Server's autopost channel set to " + str(channel) + "."))
    
    @autopost_set.command(name="location")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def set_location(self, ctx: commands.Context, *, location: str) -> None:
        """
        Sets the location (city) to autopost weather forecast data for (no default; must be set).
        
        example: `[p]autopostset location Melbourne,AU`
        example: `[p]autopostset location Tokyo`
        """
        guild = ctx.message.guild
        await self.config.guild(guild).autopostlocation.set(location)
        await ctx.send(_("Server's autopost location set to " + location + "."))
        
    @checks.mod_or_permissions(manage_messages=True)
    @commands.group(name="autopost_switch")
    async def autopost_switch(self, ctx: commands.Context) -> None:
        """
        Toggle autoposting on or off.
        
        example: `[p]autopost_switch on`
        """
        pass

    @autopost_switch.command(name="on")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def switch_on(self, ctx: commands.Context) -> None:
        """
        Turns on autoposting.
        """
        guild = ctx.message.guild
        await self.config.guild(guild).autopoststate.set(True)
        await ctx.send(_("Autopost switch turned on."))

    @autopost_switch.command(name="off")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def switch_off(self, ctx: commands.Context) -> None:
        """
        Turns off autoposting.
        """
        guild = ctx.message.guild
        await self.config.guild(guild).autopoststate.set(False)
        await ctx.send(_("Autopost switch turned off."))

    # async def get_weather_short(
        # self,
        # ctx: commands.Context,
        # *,
        # location: Optional[str] = None,
        # zipcode: Optional[str] = None,
        # cityid: Optional[int] = None,
    # ) -> None:
        # guild = ctx.message.guild
        # author = ctx.message.author
        
        ##figure out units (degrees C/F)
        # bot_units = await self.config.units()
        # guild_units = None
        # if guild:
            # guild_units = await self.config.guild(guild).units()
        # user_units = await self.config.user(author).units()
        # units = "metric"#default to C, not F
        # if bot_units:
            # units = bot_units
        # if guild_units:
            # units = guild_units
        # if user_units:
            # units = user_units
        
        ##construct the URL to query weather API with
        # params = {"appid": "614dad22d76feee3c9a8126044290e07", "units": units}#separate free-tier API key; not TrustyJAID's
        
        # if zipcode:
            # params["zip"] = str(zipcode)
        # elif cityid:
            # params["id"] = str(cityid)
        # else:
            # params["q"] = str(location)
        
        # url = "https://api.openweathermap.org/data/2.5/forecast?{0}".format(urlencode(params))
        
        ##query weather API with constructed URL
        # async with aiohttp.ClientSession() as session:
            # async with session.get(url) as resp:
                # data = await resp.json()
        # try:
            # if data["message"] == "city not found":
                # await ctx.send("City not found.")
                # return
        # except Exception:
            # pass
        
        ##figure out values for main message
        # forecast_temp = data["list"][0]["main"]["temp"]
        # forecast_feels = data["list"][0]["main"]["feels_like"]
        # city = data["city"]["name"]
        # try:
            # country = data["city"]["country"]
        # except KeyError:
            # country = ""
        ##condition = ", ".join(info["main"] for info in data["list"][0]["weather"])#one-word version
        # condition = ", ".join(info["description"] for info in data["list"][0]["weather"])#short phrase version

        ##construct main message using previous values
        # embed = discord.Embed(colour=discord.Colour.dark_blue())
        
        ##since this isn't a reaction (but its own message), I guess using :emoji: is actually okay?
        ##https://discordpy.readthedocs.io/en/latest/faq.html
        # if len(city) and len(country):
            # countrycodeleft = country[0].lower()
            # countrycoderight = country[1].lower()
            # flagcode = ":flag_" + countrycodeleft + countrycoderight + ":"
            # embed.add_field(name=_(flagcode + " **Location**"), value="{0}, {1}".format(city, country))
        # else:
            # embed.add_field(
                # name=_("\N{EARTH GLOBE AMERICAS} **Location**"),
                # value=_("*Unavailable*")
            # )
        
        ##dynamic weather emoji ::fingerguns::
        ##weatheremoji = "\N{WHITE SUN WITH SMALL CLOUD}"#default
        # weatheremoji = "❓"#better default for testing, and also diagnostically useful if the icon data changes
        
        # weathericon = data["list"][0]["weather"][0]["icon"]
        ##if weathericon == "01d":
        ##    weatheremoji = "☀"
        ##elif weathericon == "01n":
        ##    weatheremoji = "🌙"
        ##elif "02" in weathericon:
        ##    weatheremoji = "🌤"
        ##elif "03" in weathericon:
        ##    weatheremoji = "🌥"
        ##elif "04" in weathericon:
        ##    weatheremoji = "☁"
        ##elif "09" in weathericon:
        ##    weatheremoji = "🌧"
        ##elif "10" in weathericon:
        ##    weatheremoji = "🌦"
        ##elif "11" in weathericon:
        ##    weatheremoji = "⛈"
        ##elif "13" in weathericon:
        ##    weatheremoji = "❄"
        ##elif "53" in weathericon:
        ##    weatheremoji = "🌫"
            
        # if weathericon == "01d":
            # weatheremoji = ":sunny:"
        # elif weathericon == "01n":
            # weatheremoji = ":crescent_moon:"
        # elif "02" in weathericon:
            # weatheremoji = ":white_sun_cloud:"
        # elif "03" in weathericon:
            # weatheremoji = ":white_sun_small_cloud:"
        # elif "04" in weathericon:
            # weatheremoji = ":cloud:"
        # elif "09" in weathericon:
            # weatheremoji = ":cloud_rain:"
        # elif "10" in weathericon:
            # weatheremoji = ":white_sun_rain_cloud:"
        # elif "11" in weathericon:
            # weatheremoji = ":cloud_rain:"
        # elif "13" in weathericon:
            # weatheremoji = ":snowflake:"
        # elif "53" in weathericon:
            # weatheremoji = ":fog:"
        # elif "50" in weathericon:
            # weatheremoji = ":fog:"
        
        # embed.add_field(
            # name=_(weatheremoji + " **Forecast**"),
            # value="{0:.2f}{1} (feels like {2:.2f}{3}),\n{4}".format(
                # forecast_temp, self.unit[units]["temp"],
                # forecast_feels, self.unit[units]["temp"],
                # condition
            # ),
        # )
        
        ##message footer
        # embed.set_footer(text=_("Powered by https://openweathermap.org"))
        
        ##send constructed message
        # await ctx.send(embed=embed)

    async def get_weather_forecast(
        self,
        ctx: commands.Context,
        *,
        location: Optional[str] = None,
        zipcode: Optional[str] = None,
        cityid: Optional[int] = None,
    ) -> None:
        guild = ctx.message.guild
        author = ctx.message.author
        
        # figure out units (degrees C/F)
        bot_units = await self.config.units()
        guild_units = None
        if guild:
            guild_units = await self.config.guild(guild).units()
        user_units = await self.config.user(author).units()
        units = "metric"#default to C, not F
        if bot_units:
            units = bot_units
        if guild_units:
            units = guild_units
        if user_units:
            units = user_units
        
        # construct the URL to query weather API with
        params = {"appid": "88660f6af079866a3ef50f491082c386", "units": units}#TrustyJAID's API key!
        
        if zipcode:
            params["zip"] = str(zipcode)
        elif cityid:
            params["id"] = str(cityid)
        else:
            params["q"] = str(location)
        
        url = "https://api.openweathermap.org/data/2.5/forecast/daily?{0}".format(urlencode(params))
        
        # query weather API with constructed URL
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
        try:
            if data["message"] == "city not found":
                await ctx.send("City not found.")
                return
        except Exception:
            pass
        
        # figure out values for main message
        forecast_min = data["list"][1]["temp"]["min"]
        forecast_max = data["list"][1]["temp"]["max"]
        city = data["city"]["name"]
        try:
            country = data["city"]["country"]
        except KeyError:
            country = ""
        #condition = ", ".join(info["main"] for info in data["list"][0]["weather"])#one-word version
        condition = ", ".join(info["description"] for info in data["list"][1]["weather"])#short phrase version

        # construct main message using previous values
        embed = discord.Embed(colour=discord.Colour.dark_blue())
        
        # since this isn't a reaction (but its own message), I guess using :emoji: is actually okay?
        # https://discordpy.readthedocs.io/en/latest/faq.html
        if len(city) and len(country):
            countrycodeleft = country[0].lower()
            countrycoderight = country[1].lower()
            flagcode = ":flag_" + countrycodeleft + countrycoderight + ":"
            embed.add_field(name=_(flagcode + " **Location**"), value="{0}, {1}".format(city, country))
        else:
            embed.add_field(
                name=_("\N{EARTH GLOBE AMERICAS} **Location**"),
                value=_("*Unavailable*")
            )
        
        # dynamic weather emoji ::fingerguns::
        #weatheremoji = "\N{WHITE SUN WITH SMALL CLOUD}"#default
        weatheremoji = "❓"#better default for testing, and also diagnostically useful if the icon data changes
        
        weathericon = data["list"][1]["weather"][0]["icon"]
            
        if weathericon == "01d":
            weatheremoji = ":sunny:"
        elif weathericon == "01n":
            weatheremoji = ":crescent_moon:"
        elif "02" in weathericon:
            weatheremoji = ":white_sun_cloud:"
        elif "03" in weathericon:
            weatheremoji = ":white_sun_small_cloud:"
        elif "04" in weathericon:
            weatheremoji = ":cloud:"
        elif "09" in weathericon:
            weatheremoji = ":cloud_rain:"
        elif "10" in weathericon:
            weatheremoji = ":white_sun_rain_cloud:"
        elif "11" in weathericon:
            weatheremoji = ":cloud_rain:"
        elif "13" in weathericon:
            weatheremoji = ":snowflake:"
        elif "53" in weathericon:
            weatheremoji = ":fog:"
        elif "50" in weathericon:
            weatheremoji = ":fog:"
        
        embed.add_field(
            name=_(weatheremoji + " **Tomorrow**"),
            value="{0:.2f}-{1:.2f}{2},\n{3}".format(
                forecast_min, forecast_max,
                self.unit[units]["temp"], condition
            ),
        )
        
        # message footer
        embed.set_footer(text=_("Powered by https://openweathermap.org"))
        
        # send constructed message
        await ctx.send(embed=embed)

    async def get_weather_current(
        self,
        ctx: commands.Context,
        *,
        location: Optional[str] = None,
        zipcode: Optional[str] = None,
        cityid: Optional[int] = None,
    ) -> None:
        guild = ctx.message.guild
        author = ctx.message.author
        
        # figure out units (degrees C/F)
        bot_units = await self.config.units()
        guild_units = None
        if guild:
            guild_units = await self.config.guild(guild).units()
        user_units = await self.config.user(author).units()
        units = "metric"#default to C, not F
        if bot_units:
            units = bot_units
        if guild_units:
            units = guild_units
        if user_units:
            units = user_units
        
        # construct the URL to query weather API with
        params = {"appid": "614dad22d76feee3c9a8126044290e07", "units": units}#separate free-tier API key; not TrustyJAID's
        
        if zipcode:
            params["zip"] = str(zipcode)
        elif cityid:
            params["id"] = str(cityid)
        else:
            params["q"] = str(location)
        
             # https://api.openweathermap.org/data/2.5/weather?q={city name},{country code}&appid={API key}
        url = "https://api.openweathermap.org/data/2.5/weather?{0}".format(urlencode(params))
        
        # query weather API with constructed URL
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
        try:
            if data["message"] == "city not found":
                await ctx.send("City not found.")
                return
        except Exception:
            pass
        
        # figure out values for main message
        current_temp = data["main"]["temp"]
        current_feels = data["main"]["feels_like"]
        city = data["name"]
        try:
            country = data["sys"]["country"]
        except KeyError:
            country = ""
        condition = ", ".join(info["description"] for info in data["weather"])#short phrase version

        # construct main message using previous values
        embed = discord.Embed(colour=discord.Colour.blue())
        
        # since this isn't a reaction (but its own message), I guess using :emoji: is actually okay?
        # https://discordpy.readthedocs.io/en/latest/faq.html
        if len(city) and len(country):
            countrycodeleft = country[0].lower()
            countrycoderight = country[1].lower()
            flagcode = ":flag_" + countrycodeleft + countrycoderight + ":"
            embed.add_field(name=_(flagcode + " **Location**"), value="{0}, {1}".format(city, country))
        else:
            embed.add_field(
                name=_("\N{EARTH GLOBE AMERICAS} **Location**"),
                value=_("*Unavailable*")
            )
        
        # dynamic weather emoji ::fingerguns::
        weatheremoji = "❓"
        
        weathericon = data["weather"][0]["icon"]
            
        if weathericon == "01d":
            weatheremoji = ":sunny:"
        elif weathericon == "01n":
            weatheremoji = ":crescent_moon:"
        elif "02" in weathericon:
            weatheremoji = ":white_sun_cloud:"
        elif "03" in weathericon:
            weatheremoji = ":white_sun_small_cloud:"
        elif "04" in weathericon:
            weatheremoji = ":cloud:"
        elif "09" in weathericon:
            weatheremoji = ":cloud_rain:"
        elif "10" in weathericon:
            weatheremoji = ":white_sun_rain_cloud:"
        elif "11" in weathericon:
            weatheremoji = ":cloud_rain:"
        elif "13" in weathericon:
            weatheremoji = ":snowflake:"
        elif "53" in weathericon:
            weatheremoji = ":fog:"
        elif "50" in weathericon:
            weatheremoji = ":fog:"
        
        embed.add_field(
            name=_(weatheremoji + " **Current weather**"),
            value="{0:.2f}{1} (feels like {2:.2f}{3}),\n{4}".format(
                current_temp, self.unit[units]["temp"],
                current_feels, self.unit[units]["temp"],
                condition
            ),
        )
        
        # message footer
        embed.set_footer(text=_("Powered by https://openweathermap.org"))
        
        # send constructed message
        await ctx.send(embed=embed)

    async def autopost_loop(
        self,
        ctx: commands.Context
    ) -> None:
        guild = ctx.message.guild
        author = ctx.message.author
        channel = ctx.message.channel
    
        # wait for bot to be loaded etc
        await self.bot.wait_until_ready()
        
        # do the loop
        while "Autopost" in self.bot.cogs:
            
            # if autoposting is enabled, then autopost
            if await self.config.guild(guild).autopoststate():
                # to save resources, we *copy* the value of settings *outside* of the loop
                # this means we don't risk repeatedly reading the source value (which is slower)
                posting_time = await self.config.guild(guild).autoposttime()
                posting_channel = await self.config.guild(ctx.guild).autopostchannel()
                location = await self.config.guild(guild).autopostlocation()
                
                # perform check on autopost channel
                # if there's no channel, set default to where the autopost command was sent
                if posting_channel == "":
                    await self.config.guild(ctx.guild).autopostchannel.set(ctx.channel.id)#make >this< channel the saved channel if nothing is set
                    await ctx.send("No autopost channel was set, defaulting to current channel. This can be changed using `[p]autopostset channel`")
                else:
                    pass
        
                # perform check on autopost location
                # if there's no location, notify user and abort
                if location == "":
                    await ctx.send("No location specified. Use `[p]autopostset location`.")
                    return
                else:
                    pass
                    
                # perform check on autopost time
                # if there's no value, set the value to current time
                if posting_time == "":
                    posting_time = datetime.now().timestamp()
                    await self.config.guild(guild).autoposttime.set(posting_time)
                    await ctx.send("No autopost time was set, defaulting to current time. This can be changed using `[p]autopostset time.`")
                else:
                    pass
                
                # convert time from string to int for comparison purposes
                posting_time = int(posting_time)
                
                # figure out units (degrees C/F)
                bot_units = await self.config.units()
                guild_units = None
                if guild:
                    guild_units = await self.config.guild(guild).units()
                user_units = await self.config.user(author).units()
                units = "metric"#default to C, not F
                if bot_units:
                    units = bot_units
                if guild_units:
                    units = guild_units
                if user_units:
                    units = user_units
                
                while datetime.now().timestamp() > posting_time:
                
                    await ctx.typing()
                    
                    # construct the URL to query weather API with
                    params = {"appid": "88660f6af079866a3ef50f491082c386", "units": units}#TrustyJAID's API key!
                    params["q"] = str(location)#other methods for weather format not supported in autopost
                            
                    url = "https://api.openweathermap.org/data/2.5/forecast/daily?{0}".format(urlencode(params))
                    
                    # query weather API with constructed URL
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as resp:
                            data = await resp.json()
                    try:
                        if data["message"] == "city not found":
                            await ctx.send("City not found.")
                            return
                    except Exception:
                        pass
                            
                    # moved this check to start to improve responsiveness / performance on-error
                    try:
                        country = data["city"]["country"]
                    except KeyError:
                        country = ""
                            
                    # figure out values for main message
                    mintemp = data["list"][0]["temp"]["min"]
                    maxtemp = data["list"][0]["temp"]["max"]
                    weathertext = data["list"][0]["weather"][0]["description"]
                    clouds = data["list"][0]["clouds"]
                    probprecip = data["list"][0]["pop"]
                    
                    morn = data["list"][0]["temp"]["morn"]
                    day = data["list"][0]["temp"]["day"]
                    eve = data["list"][0]["temp"]["eve"]
                    night = data["list"][0]["temp"]["night"]
                    mornfeels = data["list"][0]["feels_like"]["morn"]
                    dayfeels = data["list"][0]["feels_like"]["day"]
                    evefeels = data["list"][0]["feels_like"]["eve"]
                    nightfeels = data["list"][0]["feels_like"]["night"]
                    city = data["city"]["name"]
                    today = datetime.today().strftime("%A, %d %B")
                    
                    # values for the embed fields
                    day1 = datetime.today() + timedelta(1)
                    day1f = day1.strftime("%A")
                    day2 = datetime.today() + timedelta(2)
                    day2f = day2.strftime("%A")
                    day3 = datetime.today() + timedelta(3)
                    day3f = day3.strftime("%A")
                    min1 = data["list"][1]["temp"]["min"]
                    max1 = data["list"][1]["temp"]["day"]
                    min2 = data["list"][2]["temp"]["min"]
                    max2 = data["list"][2]["temp"]["day"]
                    min3 = data["list"][3]["temp"]["min"]
                    max3 = data["list"][3]["temp"]["day"]
                    weathertext1 = data["list"][1]["weather"][0]["description"]
                    weathertext2 = data["list"][2]["weather"][0]["description"]
                    weathertext3 = data["list"][3]["weather"][0]["description"]
                    
                    # construct main message using previous values
                    embed = discord.Embed()
                    
                    embed.colour = discord.Colour.blue()
                    embed.title = city + ", " + today
                    
                    descmain1 = "**High:** {0:.1f}{1} / **Low:** {2:.1f}{1},".format(maxtemp, self.unit[units]["temp"], mintemp)
                    descmain2 = "{0}".format(weathertext)#weird code-formatting choice because earlier versions were different (and later versions might be too!)
                    descmain3 = "{0:.0f}% cloudy, {1:.0f}% pop".format(clouds, probprecip)
                    descmain = descmain1 + "\n" + descmain2 + ", " + descmain3#should add an if/else that adds rain/snow etc in mm if it exists in the data e.g. 95% pop (3mm rain)
                    
                    desc1 = "**Morning:** {0:.1f} (feels {2:.1f}){1}".format(morn, self.unit[units]["temp"], mornfeels)
                    desc2 = "**Day:** {0:.1f} (feels {2:.1f}){1}".format(day, self.unit[units]["temp"], dayfeels)
                    desc3 = "**Evening:** {0:.1f} (feels {2:.1f}){1}".format(eve, self.unit[units]["temp"], evefeels)
                    desc4 = "**Night:** {0:.1f} (feels {2:.1f}){1}".format(night, self.unit[units]["temp"], nightfeels)
                    
                    embed.description = descmain + "\n\n" + desc1 + "\n" + desc2 + "\n" + desc3 + "\n" + desc4
                    
                    embed.add_field(name=_(day1f), value="**High:** {0:.1f} / **Low:** {2:.1f},\n{3}".format(max1, self.unit[units]["temp"], min1, weathertext1))
                    embed.add_field(name=_(day2f), value="**High:** {0:.1f} / **Low:** {2:.1f},\n{3}".format(max2, self.unit[units]["temp"], min2, weathertext2))
                    embed.add_field(name=_(day3f), value="**High:** {0:.1f} / **Low:** {2:.1f},\n{3}".format(max3, self.unit[units]["temp"], min3, weathertext3))
                    
                    # message footer
                    embed.set_footer(text=_("Powered by https://openweathermap.org"))
                    
                    # send constructed message
                    sendchannel = ctx.guild.get_channel(int(posting_channel))
                    await sendchannel.send(embed=embed)
                    
                    # increment the value of posting_time by 24 hours until it exceeds the current time
                    # (this approach is helpful if the bot is ever offline for more than a day at a time)
                    while datetime.now().timestamp() > posting_time:
                        posting_time += 86400
                    
                    # save the posting_time value to file
                    await self.config.guild(guild).autoposttime.set(posting_time)
            else:
                pass
            
            # wait for a while (whether or not we autoposted)
            await asyncio.sleep(5)
