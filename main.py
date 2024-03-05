import disnake
from disnake.ext import commands

import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all(),
                   activity=disnake.Game("PyCharm", status=disnake.Status.online))

conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    num_msg INTEGER,
    insertion_date TEXT)""")
conn.commit()

bot.remove_command("help")

bot.load_extension("cogs.slash_commands")
bot.load_extension("cogs.events")

bot.run(token=TOKEN)
