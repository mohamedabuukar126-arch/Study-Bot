import discord
from discord import app_commands
from discord.ext import commands
import traceback
import asyncio
import random
import time

# loads the user database and we will be using the database to store anything in general
from Study_Bot.database import database as db


# admin whitelist
ADMIN_WHITELIST = [1265426408793182239]




# defines the guild id
GUILD_ID = 1491953788611985419

class admin(commands.Cog):
    def __init__(self, bot):
      self.bot = bot


    @app_commands.command(name="resetuser", description="Resets a user's data")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def resetuser(self, interaction: discord.Interaction, user: discord.User):

        # checks if the user is in the admin whitelist
        if interaction.user.id not in ADMIN_WHITELIST:
            await interaction.response.send_message("You are not allowed to use this command!")
            return

        # resets the user's data
        await interaction.response.send_message(f"Resetting {user.name}'s data...")
        db.delete_user(user.id)
        db.delete_study(user.id)
        await interaction.followup.send(f"{user.name}'s data has been reset!")
        return
    





        





    

        
    

        
    





    



       
        
        

        
        


       

        


 



































































































# the steup at the bottom to link the cog
async def setup(bot):
     await bot.add_cog(admin(bot))
