from .ronpicker import RonPicker

async def setup(bot):
    await bot.add_cog(RonPicker(bot))