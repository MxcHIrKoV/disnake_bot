import disnake
from disnake.ext import commands


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Бот готов к работе!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        role = guild.get_role(1174676470245900368)
        channel = guild.get_channel(1213894738801852447)
        embed = disnake.Embed(title="🤢", description=f"{member.name}")

        await channel.send(embed=embed)
        await member.add_roles(role)

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     guild = message.guild
    #     channel = guild.get_channel(1213894738801852447)
    #
    #     if message.author.bot == False:
    #         await channel.send(f"<@{message.author.id}> : {message.content}")
    #         print(message)


def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
    print(f">Extension {__name__} is ready")
