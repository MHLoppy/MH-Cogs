from .ronrobtauntsmanual import RonRobTauntsManual

async def setup(bot):
    await bot.add_cog(RonRobTauntsManual(bot))