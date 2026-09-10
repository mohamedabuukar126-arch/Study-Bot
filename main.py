
from fileinput import filename
from gc import DEBUG_STATS
import discord
from discord.ext import commands
import os
import traceback
from Study_Bot import config
import random
import asyncio
import datetime
import requests
from dotenv import load_dotenv
import time
from threading import Thread
from flask import Flask

from Study_Bot.AI_Model.ai import ask_ai
from Study_Bot.database.database import get_db, create_tables


# Creates the database tables
create_tables()

# Load environment variables
load_dotenv()

# Forces Python to use the current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))


TOKEN = os.getenv("TOKEN")
GUILD_ID = 1491953788611985419

ADMIN_WHITELIST = [1265426408793182239]

intents = discord.Intents.default()
intents.message_content = True


def pretty_error(err):
    return "".join(
        traceback.format_exception(type(err), err, err.__traceback__)
    )


class MyBot(commands.Bot):
    async def setup_hook(self):
        cogs_path = os.path.join(
            os.getcwd(),
            "Study_Bot",
            "cogs"
        )

        try:
            for filename in os.listdir("./Study_Bot/cogs"):
                if filename.endswith(".py") and filename != "__init__.py":
                    await self.load_extension(
                        f"Study_Bot.cogs.{filename[:-3]}"
                    )

        except Exception as e:
            print("❌ COG LOAD ERROR")
            print(pretty_error(e))

    async def interaction_check(self, interaction: discord.Interaction):
        if (
            config.MAINTENANCE_MODE
            and interaction.user.id not in config.ADMIN_WHITELIST
        ):
            await interaction.response.send_message(
                "🛠️ Study Bot is currently under maintenance.\n\n"
                "Please check back later!",
                ephemeral=True
            )
            return False

        return True


bot = MyBot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    try:
        guild = discord.Object(id=GUILD_ID)

        synced = await bot.tree.sync(guild=guild)

        print(f"Synced {len(synced)} commands to guild")
        print(f"Logged in as {bot.user}")

    except Exception as e:
        print("❌ SYNC ERROR")
        print(pretty_error(e))


# --------------------------------------------------
# Render Web Service
# --------------------------------------------------

app = Flask(__name__)


@app.route("/")
def home():
    return "Study Bot is running!"


def run_web_server():
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )


# Start the web server in the background
Thread(
    target=run_web_server,
    daemon=True
).start()


# --------------------------------------------------
# Start Discord Bot
# --------------------------------------------------

if not TOKEN:
    print("❌ TOKEN missing in Secrets!")
else:
    bot.run(TOKEN)

