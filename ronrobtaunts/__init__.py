from .ronrobtaunts import RonRobTaunts

def setup(bot):
    n = RonRobTaunts(bot)
    bot.add_cog(n)
