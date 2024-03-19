from .ronrobtaunts import RonRobTaunts

async def setup(bot):
    await bot.add_cog(RonRobTaunts(bot))