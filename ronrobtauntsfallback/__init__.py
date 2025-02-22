from .ronrobtauntsfallback import RonRobTauntsFallback

async def setup(bot):
    await bot.add_cog(RonRobTauntsFallback(bot))