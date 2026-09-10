import discord
from discord import app_commands
from discord.ext import commands
import traceback
import json
import asyncio
import random
import sqlite3
import time
import Study_Bot.database.database as db
import Study_Bot.AI_Model.ai as AI_Model


# defines the guild id
GUILD_ID = 1491953788611985419

class fun(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
      self.activate_debates = {}

    @app_commands.command(name="sillychecker", description="Checks if you are silly. This is a joke command")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def sillychecker(self, interaction: discord.Interaction):

      # checkkkk
        await interaction.response.send_message("Checking.....")
        await asyncio.sleep(3)

        # random chance of being silly
        output = random.choice(["You are silly", "You are not silly"])
        await interaction.followup.send(output)
        if output == "You are silly":
           await interaction.followup.send("https://tenor.com/view/snoopy-laughing-giggling-silly-funny-gif-16011534249941914272")
           return
        if output == "You are not silly":
           await interaction.followup.send("https://tenor.com/view/shock-gif-27193002")
           return

    @app_commands.command(name="choose", description="Choose between two options")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def choose(self, interaction: discord.Interaction, option1: str, option2: str, option3: str):

      # random choice between the three options
      random_choice = random.choice([option1, option2, option3])

      output = f"I choose {random_choice}!"


      await interaction.response.send_message(output)

    @app_commands.command(name="sendatiktok", description="Send a tiktok to the channel. You will be asked to enter a tiktok link.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def sendatiktok(self, interaction: discord.Interaction):

     # tells discord to wait
     await interaction.response.defer(thinking=True)

     # tells the user to type the tiktok link
     await interaction.followup.send("Please enter the tiktok link you want to send.")



     # waits for the user to send the tiktok link
     def check(m):
       return m.author == interaction.user and m.channel == interaction.channel

     try:
       msg = await self.bot.wait_for('message', check=check, timeout=30.0)

       # checks if the message is a tiktok link
       if "www.tiktok.com" in msg.content:
         await interaction.followup.send("Sending tiktok...")
         # puts kk before tiktok.com
         new_url = msg.content.replace("www.tiktok.com", "www.kktiktok.com")
         await interaction.followup.send(f"Here is your tiktok link: {new_url}")
       else:
         await interaction.followup.send("Please enter a valid tiktok link.")
         return
     except asyncio.TimeoutError:
       await interaction.followup.send("You took too long to respond. Cancelled.")
       return

    @app_commands.command(name="ship", description="ships two people together. This is a joke command")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def ship(self, interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):

      # checks if the bot is trying to ship the same person with themselves
      if user1 == user2:
          await interaction.response.send_message("You cannot ship the same person with themselves.")
          return
      
      # checks if the user is trying to ship the bot with themselves
      if user1 == self.bot.user or user2 == self.bot.user:
          await interaction.response.send_message("You cannot ship the bot with yourself. Its not a good idea.")
          return
      
      # random chance of shipping the two people together
      random_chance = random.randint(1, 100)

      # outputs the random chance
      output = f"{user1.mention} and {user2.mention} have a {random_chance}% chance of being together!"
      await interaction.response.send_message(output)
      if random_chance > 50:
         await interaction.followup.send("https://tenor.com/view/slap-gif-22200436")
         return
      if random_chance < 50:
         await interaction.followup.send("https://tenor.com/view/anime-anime-blush-anime-couple-horimiya-anime-slap-gif-8899682970938832274")
         return
      if random_chance == 100:
         await interaction.followup.send("https://tenor.com/view/kiss-anime-kiss-anime-gif-27284749")
         return
      if random_chance == 0:
         await interaction.followup.send("https://tenor.com/view/death-note-misora-naomi-misora-naomi-death-stare-gif-7312237509524715724")
         return

    @app_commands.command(name="ping", description="Ping the bot and see how long it takes to respond")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def ping(self, interaction: discord.Interaction):

      # get the bot latency
      latency = round(self.bot.latency * 1000)
      await interaction.response.send_message(f"Pong! {latency}ms")
      return

    @app_commands.command(name="detectlie", description="🔍 Lie Analysis. This is a joke command")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def detectlie(self, interaction: discord.Interaction, lie: str):

      # tells the user that the AI model is thinking
      await interaction.response.defer()
      await interaction.followup.send("Thinking...")
      await asyncio.sleep(1)

      # asks the AI model the question
      response = AI_Model.lie_detect(interaction.user.id, lie)
      
      #sends the response
      await interaction.followup.send(response)
      return

    @app_commands.command(name="clearmemory", description="Clear the AI model's memory. If its not cleared, the AI model will remember everything you say.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def clearmemory(self, interaction: discord.Interaction):

      # clears the AI model's memory
      await interaction.response.send_message("Are you sure you want to clear the AI model's memory? (yes/no)")

      # checks if the user even has memory
      if db.check_datasaving(interaction.user.id) == 0:
        await interaction.followup.send("You don't have any memory to clear!")
        return
        

      

   
      
      
      # waits for the user to send their answer 
      def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

      try:
        msg = await self.bot.wait_for('message', check=check, timeout=30.0)

        if msg.content.lower() == "yes":
          await interaction.followup.send("Clearing memory...")
          await asyncio.sleep(1)
          db.clear_memory(interaction.user.id)
          print("Memory cleared for user:", interaction.user.id)
          await interaction.followup.send("Memory cleared!")
          return
        else:
          await interaction.followup.send("Cancelled.")
          return
      except asyncio.TimeoutError:
        await interaction.followup.send("You took too long to respond. Cancelled.")
        return

    @app_commands.command(name="debate", description = "Debate with the AI model.")
    @app_commands.describe(topic = "The topic you want to debate on", side = "Choose 1 for FOR and 2 for AGAINST")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def debate(self, interaction: discord.Interaction, topic: str, side: int): 

      # store the user side
      user_side = side
      ai_side = None
      user_argument = None

      # whatever side the user chooses, the AI model will choose the opposite side
      if user_side == 1:
        user_side = "FOR"
        ai_side = "AGAINST"
      elif user_side == 2:
        user_side = "AGAINST"
        ai_side = "FOR"
      else:
        await interaction.response.send_message("Please choose a valid side. 1 is for and 2 is against.")
        return

      # Tells the user if they type End Debate, the debate will end
      await interaction.response.send_message("Use the End Debate command to end the debate at any time.")
      await asyncio.sleep(3)
      await interaction.followup.send("Starting debate...")
      
      # Round One AI Arugment
      await interaction.followup.send(f"Round 1: AI is {ai_side} {topic} and you are {user_side} {topic}")
      await asyncio.sleep(2)
      await interaction.followup.send("AI is writing its argument...")
      await asyncio.sleep(2)
      response = AI_Model.debate(interaction.user.id, topic, ai_side, user_argument = None, round = 1)
      await interaction.followup.send(response)

      

      # store the AI argument for Round 1
      ai_argument1 = response
      
      
      

      # Round One User Argument
      await interaction.followup.send(f"Round 1: You are {user_side} {topic}. Please enter your argument.")
      await asyncio.sleep(2)
      await interaction.followup.send("You have 5 minutes to respond.")
      def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

      try:
        task = asyncio.create_task(self.bot.wait_for('message', check=check, timeout=300.0))
        self.activate_debates[interaction.user.id] = task
        msg = await task
        await interaction.followup.send(f"You said: {msg.content}")
        await asyncio.sleep(1)
        user_argument = msg.content
        # checks how long is left

      except asyncio.TimeoutError:
        await interaction.followup.send("You took too long to respond. Cancelled.")
        return

      # store the user argument for Round 1
      user_argument1 = msg.content


      # Round Two AI Argument
      await interaction.followup.send(f"Round 2: AI is {ai_side} {topic}")
      await asyncio.sleep(2)
      await interaction.followup.send("AI is writing its argument...")
      await asyncio.sleep(2)
      response = AI_Model.debate(interaction.user.id, topic, ai_side, user_argument1, round = 2)
      await interaction.followup.send(response)
                                 

      # Round Two User Argument
      await interaction.followup.send(f"Round 2: You are {user_side} {topic}. Please enter your argument.")
      await asyncio.sleep(2)
      await interaction.followup.send("You have 5 minutes to respond.")
      await asyncio.sleep(2)

      try:
         task = asyncio.create_task(self.bot.wait_for('message', check=check, timeout=300.0))
         self.activate_debates[interaction.user.id] = task
         msg = await task
         await interaction.followup.send(f"You said: {msg.content}")
         await asyncio.sleep(2)
         user_argument = msg.content
         # checks how long is left
      except asyncio.TimeoutError:
        await interaction.followup.send("You took too long to respond. Cancelled.")
        return

      # store the AI argument for Round 2 and the user argument for Round 2
      ai_argument2 = response
      user_argument2 = msg.content
      
  

      # Round Three AI Argument
      await interaction.followup.send(f"Round 3: AI is {ai_side} {topic}")
      await asyncio.sleep(2)
      await interaction.followup.send("AI is writing its argument...")
      await asyncio.sleep(2)
      response = AI_Model.debate(interaction.user.id, topic, ai_side, user_argument2, round = 3)
      await interaction.followup.send(response)

      # Round Three User Argument
      await interaction.followup.send(f"Round 3: You are {user_side} {topic}. Please enter your argument.")
      await asyncio.sleep(2)
      await interaction.followup.send("You have 5 minutes to respond.")
      try:
         task = asyncio.create_task(self.bot.wait_for('message', check=check, timeout=300.0))
         self.activate_debates[interaction.user.id] = task
         msg = await task
         await interaction.followup.send(f"You said: {msg.content}")
         await asyncio.sleep(1)
         user_argument = msg.content
         # checks how long is left
      except asyncio.TimeoutError:
        await interaction.followup.send("You took too long to respond. Cancelled.")
        return

      # store the AI argument for Round 2 and the user argument for Round 2
      ai_argument3 = response
      user_argument3 = msg.content

      # AI judges the winner
      await interaction.followup.send("AI is judging the winner...")
      await asyncio.sleep(1)
      response = AI_Model.judge_ai(interaction.user.id, topic, ai_side, ai_argument1, ai_argument2, ai_argument3, user_argument1, user_argument2, user_argument3)
      await interaction.followup.send(response)
      return

    @app_commands.command(name="enddebate", description="End the debate")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def enddebate(self, interaction: discord.Interaction):

      # ends the debate
      if interaction.user.id in self.activate_debates:
         self.activate_debates[interaction.user.id].cancel()
         await interaction.response.send_message("Debate ended.")
         return
      else:
         await interaction.response.send_message("There is no debate to end.")
         return
      
    @app_commands.command(name="dashboard", description="View your personal study progress, stats, and achievements.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def enddebate(self, interaction: discord.Interaction):

      await interaction.response.defer()

      # users ids and name
      user_id = interaction.user.id
      user_name = interaction.user.name

      # notes
      all_notes = db.get_notes(interaction.user.id)
      total_notes = len(all_notes)

      # ai attempts showcase
      attempts = db.aiquiz_attempts(interaction.user.id)


      


      

      embed = discord.Embed(title=f"📊{user_name} Study's Dashboard", description=f"Here is the info for {user_name}", color=discord.Color.blue())
      embed.add_field(name="Name:", value=user_name, inline=False)
      embed.add_field(name="User ID:", value=user_id, inline=False)
      embed.add_field(name="AI Quiz Attempts:", value=attempts, inline=False)
      embed.add_field(name="Total Notes:", value=total_notes, inline=False)
      embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
      await interaction.followup.send(embed=embed)



      


      












      
    


    
      
    


  



    
        


















































































# the steup at the bottom to link the cog
async def setup(bot):
   await bot.add_cog(fun(bot))

