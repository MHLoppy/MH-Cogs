import json
from pathlib import Path

from .globaltimes import GlobalTimes

#with open(Path(__file__).parent / "info.json") as fp:
#    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


async def setup(bot):
    n = GlobalTimes(bot)
    await bot.add_cog(n)
