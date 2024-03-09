import re
import sqlite3
import time

from DiscordLevelingCard import Settings, RankCard

import disnake
from disnake.ext import commands

from pars import anim

conn = sqlite3.connect('database.db')
cur = conn.cursor()


class SlashCommands(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.slash_command(name="помощь", description="Выводит список команд")
    async def help(self, inter):
        msg = "Здравствуйте вы прописали команду /help"
        await inter.response.send_message(msg)

    @commands.slash_command()
    async def server(self, inter):
        await inter.response.send_message(
            f"Название сервера: {inter.guild.name}\nУчастников: {inter.guild.member_count}"

        )

    @commands.slash_command(description="test")
    async def test(self, inter):
        embed = disnake.Embed(title="title", description="description", url="https://vk.com/",
                              color=disnake.Color.green())
        embed.add_field(name="name1", value="value1", inline=True)
        embed.add_field(name="name2", value="value2", inline=True)
        embed.add_field(name="name3", value="value3", inline=True)
        embed.add_field(name="name4", value="value4", inline=False)
        embed.add_field(name="name5", value="value5", inline=True)
        embed.add_field(name="name6", value="value6", inline=True)
        embed.set_image(
            url="https://desu.shikimori.one/uploads/poster/animes/54265/preview_alt_2x-1de0cbfe93df71cf7a49d46b36bd3366.jpeg")
        embed.set_author(name="name", url="https://vk.com/max.chirkov5",
                         icon_url="https://desu.shikimori.one/uploads/poster/animes/54265/preview_alt-9867d9e078891abe32b4da77910b9b68.jpeg")
        embed.set_footer(text=f"@{inter.author.name}")
        embed.set_thumbnail(
            url="https://desu.shikimori.one/uploads/poster/animes/54265/preview_alt-9867d9e078891abe32b4da77910b9b68.jpeg")
        await inter.send(embed=embed)

    @commands.slash_command(description="Очищает чат (count сообщений)")
    @commands.has_permissions(administrator=True)
    async def clear(self, inter, count: int):
        await inter.response.send_message(f"Удалено {count + 1} сообщений")
        await inter.channel.purge(limit=count + 1)

    @commands.slash_command(description="Пингует участника num количество раз")
    async def ping(self, inter, member: disnake.Member, num: int):
        for i in range(0, num):
            await inter.send(f"<@{member.id}>")

    @commands.slash_command()
    async def rename(self, inter, member: disnake.Member, rename: str):
        await inter.send(f"Ник <@{member.id}> изменен на {rename}")
        await member.edit(nick=rename)

    @commands.slash_command(name="статистика", description="Посмотреть статистику сообщений участников")
    async def stat(self, inter, member: disnake.Member = None):
        t = ""
        cur.execute("""SELECT * FROM users""")
        ctx = cur.fetchall()

        if member is None:
            t = ""
            for i in ctx:
                txt = f"<@{i[0]}> - {i[1]}\n"
                t += txt
            await inter.send(t)
        else:

            for i in ctx:
                if member.id == i[0]:
                    await inter.send(f"{member.mention} - {i[1]} сообщений")

    @commands.slash_command(name="карта", description="Посмотреть карточку")
    async def card_user(self, inter, user: disnake.Member = None):
        user = user or inter.user
        name = user.name

        photo_bg = "cogs/photo/3a232d90c53e68de2e15089aed95a67b.jpg"
        card_settings = Settings(
            background=photo_bg,
            text_color="white",
            bar_color="#5865f2"
        )

        cur.execute(f"SELECT * FROM users WHERE user_id = {user.id}")
        ctx = cur.fetchone()

        await inter.response.defer()
        a = RankCard(
            settings=card_settings,
            avatar=user.display_avatar.url,
            level=ctx[2],
            current_exp=ctx[3],
            max_exp=20,
            username=f"{name}"
        )
        image = await a.card2()
        await inter.edit_original_message(file=disnake.File(image, filename="rank.png"))

    @commands.slash_command(description="Добавляет amount опыта участнику")
    @commands.has_permissions(administrator=True)
    async def current_exp(self, inter, amount: int = 1, user: disnake.Member = None):
        user = user or inter.user

        cur.execute(f"SELECT current_exp FROM users WHERE user_id = {user.id}")
        ctx = cur.fetchone()

        num = ctx[0]
        num += amount
        cur.execute(f"""UPDATE users SET current_exp={num} WHERE user_id={user.id}""")
        conn.commit()

        cur.execute(f"SELECT user_levle, current_exp FROM users WHERE user_id = {user.id}")
        ctx1 = cur.fetchone()

        if ctx1[1] >= 20:
            current = ctx1[1] - 20

            lvl = ctx1[0]
            lvl += 1
            cur.execute(f"""UPDATE users SET user_levle={lvl}, current_exp={current} WHERE user_id={user.id}""")
            conn.commit()

        await inter.send(f"Текущий опыт {user.mention} увеличен на {amount} единиц.")

    @commands.slash_command()
    async def anim(self, inter, date: str = None):

        # embed = disnake.Embed(
        #     title=anim[0]["date"],
        #     description=anim[0]["article"]["title"]
        # )

        if date is None:

            m = []
            for anime in anim:
                if anime["date"][:21] == "Уже должно было выйти":
                    m.append(anime)
            embed = disnake.Embed(
                title=m[0]["date"],
            )
            for i in m:
                embed.add_field(name=i['article']["title"], value=f"{i['article']['series']}\n{i['article']['time']}",
                                inline=False)
                embed.set_image(url=i['article']['url_photo'])
            await inter.response.send_message(embed=embed)

        elif date == "сегодня":
            m = []
            for anime in anim:
                if anime["date"][:7] == "сегодня":
                    m.append(anime)
            embed = disnake.Embed(
                title=m[0]["date"],
            )
            for i in m:
                embed.add_field(name=i['article']["title"], value=f"{i['article']['series']}\n{i['article']['time']}",
                                inline=False)
                embed.set_image(url=i['article']['url_photo'])

            await inter.response.send_message(embed=embed)

        # elif date == (i for i in num):
        #     m = []
        #     print("Dsgjkybkjcm")
        #     for anime in anim:
        #
        #         # if anime["date"][:anime["date"].find(', ')] == re.compile(r"понедельник"):
        #         #     m.append(anime)
        #
        #         if anime["date"] == re.compile(fr"{date}"):
        #             m.append(anime)
        #
        #         # print(anime["date"][:anime["date"].find(', ')])
        #
        #     embed = disnake.Embed(
        #         title=m[0]["date"],
        #     )
        #     for i in m:
        #         embed.add_field(name=i['article']["title"], value=f"{i['article']['series']}\n{i['article']['time']}",
        #                         inline=False)
        #         embed.set_image(url=i['article']['url_photo'])
        #
        #     await inter.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(SlashCommands(bot))
    print(f">Extension {__name__} is ready")
