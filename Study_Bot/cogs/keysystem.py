import discord
from discord import app_commands
from discord.ext import commands
import traceback
import asyncio
import random
import time

# loads the user database and we will be using the database to store anything in general
import Study_Bot.database.database as db







# defines the guild id
GUILD_ID = 1491953788611985419

class keysystem(commands.Cog):
    def __init__(self, bot):
      self.bot = bot


    


        
        


       

        


 



































































































# the steup at the bottom to link the cog
async def setup(bot):
     await bot.add_cog(keysystem(bot))
