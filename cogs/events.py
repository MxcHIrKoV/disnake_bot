import disnake
from disnake.ext import commands

import datetime

import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Бот готов к работе!")

        guild = self.bot.get_guild(1112709355989647370)

        cur.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            num_msg INTEGER,
            insertion_date TEXT)""")
        conn.commit()

        for member in guild.members:
            if cur.execute(f"SELECT user_id FROM users WHERE user_id = {member.id}").fetchone() is None:
                cur.execute(f"INSERT INTO users VALUES ({member.id}, 0, '{datetime.datetime.now()}')")
                conn.commit()
            else:
                pass


    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        role = guild.get_role(1174676470245900368)
        channel = guild.get_channel(1213894738801852447)
        embed = disnake.Embed(title="🖐", description=f"Новый пользователь {member.mention}")

        if cur.execute(f"SELECT user_id FROM users WHERE user_id = {member.id}").fetchone() is None:
            cur.execute(f"INSERT INTO users VALUES ('{member.id}', 0, {datetime.datetime.now()})")
        else:
            pass
        conn.commit()

        await channel.send(embed=embed)
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = message.guild
        channel = guild.get_channel(1112709357654790205)
        user_id = message.author.id

        cur.execute(f"""SELECT num_msg FROM users WHERE user_id={user_id}""")
        num = cur.fetchall()  # [(0,)]
        num = num[0][0]
        num += 1
        cur.execute(f"""UPDATE users SET num_msg={num} WHERE user_id={user_id}""", )
        conn.commit()

        # user_id = message.author.id
        # # cur.execute("""INSERT INTO users (user_id, num_msg, insertion_date) VALUES (?, ?, ?)""",
        # #             (user_id, 0, datetime.datetime.now()))
        # # conn.commit()
        #
        # # print(members)
        # # for member in guild.members:
        # #     print(f"{member.name} ({member.global_name}) - {member.id}")


def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
    print(f">Extension {__name__} is ready")
