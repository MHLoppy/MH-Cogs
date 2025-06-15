# global-times cog by MHLoppy

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import discord
import geopy
import pytz

from geopy.geocoders import Nominatim       # https://nominatim.org/
from timezonefinder import TimezoneFinder
from datetime import datetime

class GlobalTimes(commands.Cog):
    """Posts the current time in several cities of various timezones"""

    __author__ = ["MHLoppy"]
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 695336480)#randomly generated value from random.org

    # Based on code by geekygautam1997
    def get_time_in_city(city_name):
        # Get coordinates from city name
        geolocator = Nominatim(user_agent="global_time_cog")
        location = geolocator.geocode(city_name)
    
        if location:
            lat = location.latitude
            lon = location.longitude
        
            # Get timezone using latitude and longitude
            tz_finder = TimezoneFinder()
            timezone_str = tz_finder.timezone_at(lng=lon, lat=lat)
        
            if timezone_str:
                # Get current time in that timezone
                timezone = pytz.timezone(timezone_str)
                city_time = datetime.now(timezone)
            
                cities = f"It's currently {city_time.strftime('%I:%M %p (%A)')} in {city_name}"
            else:
                cities = f"Could not find the timezone for {city_name}"
        else:
            cities = f"City {city_name} not found."
        
        return cities

    @commands.command(name="post_global_times", aliases=["times"])
    async def post_global_times(self, ctx: commands.Context):
        """
        Posts the current time in Los Angeles, New York, London, New Delhi, and Sydney.
        """
        await ctx.typing()
        city_names = ["Los Angeles", "New York", "London", "New Delhi", "Sydney"]
        cities = []
        
        for city in city_names:
            cities.append(get_time_in_city(city))
        
        cities = "\n".join(cities)
        
        embed = discord.Embed(colour=discord.Colour.white())
        embed.description = cities
        
        # Send the message
        await ctx.send(embed=embed)


