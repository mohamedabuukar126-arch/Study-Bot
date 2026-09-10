import discord
from discord import app_commands
from discord.ext import commands
import traceback
import asyncio
import random
import time
import json


# loads the user database and we will be using the database to store anything in general
import Study_Bot.database.database as db

# imports the AI model from secret
import Study_Bot.AI_Model.ai as AI_Model







# defines the guild id
GUILD_ID = 1491953788611985419

class revision(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
      self.memory_battles = {}

    @app_commands.command(name="study", description="Start studying and a timer will play ")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def study(self, interaction: discord.Interaction):

      # tells the user how long they want to study for
      await interaction.response.send_message("How long do you want to study for? (e.g. 10m, 1h)")

      # check if the user has already started a study timer
      if db.study_running(interaction.user.id):
          await interaction.followup.send("You already have a study timer running!")
          return
        
      # we create a menu for the user to choose from
      class StudyMenu(discord.ui.Select):
          def __init__(self):
              options = [
                  discord.SelectOption(label="10 minutes", value="10m"),
                  discord.SelectOption(label="1 minutes", value="1m"),
                  discord.SelectOption(label="20 minutes", value="20m"),
                  discord.SelectOption(label="30 minutes", value="30m"),
                  discord.SelectOption(label="40 minutes", value="40m"),
                  discord.SelectOption(label="50 minutes", value="50m"),
                  discord.SelectOption(label="1 hour", value="1h"),
                  discord.SelectOption(label="2 hours", value="2h"),
              ]
              super().__init__(
                  placeholder = "How long do you want to study for?",
                  min_values = 1,
                  max_values = 1,
                  options = options
              )

          # now you callback the menu
          async def callback(self, interaction: discord.Interaction):
              selected_option = self.values[0]
              await interaction.response.send_message(f"You have selected {selected_option}")
              await asyncio.sleep(2)


              # now we convert the selected option to seconds
              if selected_option.endswith("m"):
                  study_time = int(selected_option[:-1]) * 60
              elif selected_option.endswith("h"):
                  study_time = int(selected_option[:-1]) * 3600

              # save the study time in the database in total_study time
              db.save_study(interaction.user.id, study_time)

              # update it to the total study time
              db.updatetotalstudytime(interaction.user.id, study_time)
              if db.get_studytime(interaction.user.id):
                  print("It works")
              else:
                  print("It doesn't work")

              # delete the study time from the database
              db.delete_study(interaction.user.id)
              if db.delete_study(interaction.user.id):
                   print("Data deleted successfully")
              else:
                  print("Data not deleted")
                  
              

              
              
              # now we start the timer and saves the study time in the database
              await interaction.followup.send(f"Study timer started for {selected_option}")
              db.add_study(interaction.user.id, study_time)
              await asyncio.sleep(study_time)
              await interaction.followup.send(f"Study timer ended for {selected_option}")
              return
              




      class StudyView(discord.ui.View):
          def __init__(self):
              super().__init__()
              self.add_item(StudyMenu())

      await interaction.followup.send(view=StudyView())


    @app_commands.command(name="endstudy", description="End your study timer")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def endstudy(self, interaction: discord.Interaction):

        # check if the user has a study timer running
        if not db.get_studytime(interaction.user.id):
            await interaction.response.send_message("You don't have a study timer running!")
            return

        # end the study timer
        await interaction.response.send_message("Study timer ended!")
        db.delete_study(interaction.user.id)
        return

    @app_commands.command(name="studystatus", description="Calculate how long you have studied in total")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def studystatus(self, interaction: discord.Interaction):

        # calculate how long the user has studied in total
        study_time = db.get_studytime(interaction.user.id)
        if study_time is None:
            await interaction.response.send_message("You haven't studied yet!")
            return

        # convert the study time to hours and minutes
        hours = study_time // 3600
        minutes = (study_time % 3600) // 60
        await interaction.response.send_message(f"You have studied for {hours} hours and {minutes} minutes!")
        return
    
    @app_commands.command(name="reminder", description="reminds you of something")
    @app_commands.describe(reminder="What do you want to be reminded of?", duration="How long until the reminder? (e.g. 10m, 1h, 1d)")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def reminder(self, interaction: discord.Interaction, reminder: str, duration: str):

       # tells discord to wait for the command to finish
       await interaction.response.defer()

       # converts the duration from string to int
       duration_time = int(duration[:-1])

       # reminder can be in minutes, hours or even days
       if duration.endswith("m"):
         duration_time *= 60
       elif duration.endswith("h"):
         duration_time *= 3600
       elif duration.endswith("d"):
         duration_time *= 86400
       else:
         await interaction.followup.send("Invalid duration format. Use m, h, or d.", ephemeral=True)
         return

       # sends the reminder
       await interaction.followup.send(f"Reminder set for {duration}.",)
       await asyncio.sleep(duration_time)
       await interaction.user.send(f"Reminder: {reminder}")
       return



    @app_commands.command(name="listentomusic", description="Listen to music. You will be asked to enter a YouTube link.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def listentomusic(self, interaction: discord.Interaction):

        # gets the song from the user should be a youtube link
        await interaction.response.send_message("Please enter the song you want to listen to. (YouTube link)")


        # waits for the user to send the song
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)

            # checks if the message is a youtube link
            if "www.youtube.com" in msg.content:
                await interaction.followup.send(f"Playing {msg.content}")
            else:
                await interaction.followup.send("Please enter a valid YouTube link.")
                return
        except asyncio.TimeoutError:
            await interaction.followup.send("You took too long to respond. Cancelled.")
            return

    @app_commands.command(name="ask", description="You can ask the AI model a question, it will answer it for you")
    @app_commands.describe(mode = "Choose AI mode",question="What do you want to ask the AI model?")
    @app_commands.choices(mode=[
        app_commands.Choice(name="📚 Study", value="Study"),
        app_commands.Choice(name="🧠 Expert", value="Expert"),
        app_commands.Choice(name="⚡ Quick", value="Quick"),
        app_commands.Choice(name="💻 Coding", value="Coding")
    ])
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def ask(self, interaction: discord.Interaction, mode: app_commands.Choice[str], question: str):

        # tells discord to wait for the command to finish
        await interaction.response.defer(thinking=True)


        # gets the answer from the AI model
        answer = await asyncio.to_thread(AI_Model.ask_ai, user_id = interaction.user.id, question = question, mode = mode.value)


        # sends the answer to the user
        try:
            await asyncio.sleep(2)
            await interaction.followup.send(f"**Question:** {question}\n**Answer:** {answer}")
        except Exception as e:
            await interaction.followup.send(f"**Question:** {question}\n**Answer:** {answer}")
            print(f"Error sending answer: {e}")
        return
    
    @app_commands.command(name="summary", description="You can ask the AI model to summarize a text for you")
    @app_commands.describe(text="AI will summarize the text for you",)
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def summary(self, interaction: discord.Interaction, text: str):

        # tells discord to wait
        await interaction.response.defer(thinking=True)



        # gets the summary from the AI model
        summary = await asyncio.to_thread(AI_Model.summary,interaction.user.id, text = text)

        # sends the summary to the user
        try:
            await asyncio.sleep(2)
            await interaction.followup.send(f"**Summary:** {summary}")
        except Exception as e:
            await interaction.followup.send(f"**Summary:** {summary}")
            print(f"Error sending summary: {e}")
        return
    
    @app_commands.command(name="exportnotes", description="Exports your notes into text file")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def exportnotes(self, interaction: discord.Interaction):

        # tells discord to wait
        await interaction.response.defer(thinking=True)

        # gets the notes from the database
        all_notes = db.export_notes(interaction.user.id)
        print("All notes:", all_notes)


        # checks if the user has any notes
        if not all_notes:
            await interaction.followup.send("You don't have any notes to export.")
            return
        
        # creates a text file with the notes
        with open(f"{interaction.user.name}_notes.txt", "w") as f:
            for index, note in enumerate(all_notes, start=1):
                note = note.strip()
                note = f"{index}. {note}"
                f.write(note + "\n")




        # sends the text file to the user
        try:
            await asyncio.sleep(2)
            await interaction.followup.send(f"Here are your notes:", file=discord.File(f"{interaction.user.name}_notes.txt"))
        except Exception as e:
            await interaction.followup.send(f"Here are your notes:", file=discord.File(f"{interaction.user.name}_notes.txt"))
            print(f"Error sending notes: {e}")
        except Exception as e:
            await interaction.followup.send(f"Error sending notes: {e}")
            print(f"Error sending notes: {e}")
        return
    
    @app_commands.command(name="adaptive_study_plan", description="AI creates an adaptive study plan based on subject and exam date")
    @app_commands.describe(subject="What subject do you want to study?", exam_date="When is your exam?", hours_per_day="How many hours per day can you study?(Write in numbers only, e.g. 2 for 2 hours)")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def adaptive_study_plan(self, interaction: discord.Interaction, subject: str, exam_date: str, hours_per_day : int):

        # tells discord to wait
        await interaction.response.defer(thinking=True)

        # gets the adaptive study plan from the AI model
        study_plan = await asyncio.to_thread(AI_Model.study_plan,user_id = interaction.user.id, subject = subject, exam_date = exam_date)
        

        # sends the study plan to the user
        try:
            await asyncio.sleep(2)
            # if it takes long we tell the user waittt     
            await interaction.followup.send(f"**Adaptive Study Plan:** {study_plan}")
        except Exception as e:
            await interaction.followup.send(f"**Adaptive Study Plan:** {study_plan}")
            print(f"Error sending study plan: {e}")
        return
    
    @app_commands.command(name="aiquiz", description="The AI quizes you based off your notes")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def aiquiz(self, interaction: discord.Interaction):

        # tells discord to wait
        await interaction.response.defer(thinking=True)


        # gets all the notes
        all_usernotes = db.get_notes(interaction.user.id)

        # checks if the user even has notes
        if not all_usernotes:
            await interaction.followup.send("❌ You have no notes saved!")
            return

        # tells the user how it works
        await asyncio.sleep(2)
        await interaction.followup.send(
        "📚 **Your AI Quiz is starting!**\n\n"
        "🧠 **How it works:**\n"
        "• You will be given 5 questions based on your notes.\n"
        "• Answer each question by typing your answer.\n"
        "• For multiple choice questions, reply with the letter (A, B, C, or D).\n"
        "• For True/False questions, reply with True or False.\n"
        "• Your answers will be checked automatically.\n"
        "• At the end, you will receive your final score.\n\n"
        "Good luck! 🍀"
    )
        
        # get quiz from AI
        quiz = await asyncio.to_thread(AI_Model.AI_Quiz, interaction.user.id, all_usernotes)
        questions = quiz
        





        # have the score written here
        score = 0


        # check the user response
        def check(m):
            return (m.author == interaction.user and m.channel == interaction.channel)
        
        
        # loop through the quiz
        for number, q in enumerate(questions, start=1):

            message = f"❓ **Question {number}/{len(questions)}**\n\n{q['question']}\n"

            # adds choices if has them
            if "options" in q:
                message += "\n".join(q["options"])
            elif q["type"] == "true_false":
                message += "\n\nA) True\nB) False"

            await interaction.followup.send(message)


            try:
                answer = await self.bot.wait_for("message",check=check,timeout=120)


                if answer.content.lower() == str(q["answer"]).lower():
                    score += 1
                    await interaction.followup.send("✅ Correct!")
                    await asyncio.sleep(1)
                else:
                    await interaction.followup.send(
                    f"❌ Wrong! Answer: {q['answer']}")
            except asyncio.TimeoutError:
                await interaction.followup.send("⏰ Time ran out!")
                break
        await interaction.followup.send(f"Quiz finished! Score: {score}/{len(questions)}")

        # saves the quiz attempt into the attempt function
        db.saveaiquiz_attempts(interaction.user.id)
        amount = db.aiquiz_attempts(interaction.user.id)



        # now sends images cause im bored
        if score == 0:
            await asyncio.sleep(1)
            await interaction.followup.send("https://klipy.com/gifs/lock-in-twin")
        elif score == 1:
            await asyncio.sleep(1)
            await interaction.followup.send("https://klipy.com/gifs/bruh-sad-1")
        elif score == 2:
            await asyncio.sleep(1)
            await interaction.followup.send("https://klipy.com/gifs/soso-4")
        elif score == 3:
            await asyncio.sleep(1)
            await interaction.followup.send("https://klipy.com/gifs/pikanod")
        elif score == 4:
            await asyncio.sleep(1)
            await interaction.followup.send("https://klipy.com/gifs/ted-lasso-potential")
        elif score == 5:
            await asyncio.sleep(1)
            await interaction.followup.send("https://klipy.com/gifs/keep-going-75")


    @app_commands.command(name="memorybattle", description="🧠Tests your memory by creating a challenge from your notes.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def memorybattle(self, interaction: discord.Interaction):

        #debug
        print("Command Recieved")

        # tells discord to wait
        await interaction.response.defer()

        # debug
        print("Defer works i guess")

        # convert interaction.user.id into user_id
        user_id = interaction.user.id

        # pull all the notes needed
        all_usernotes = db.get_notes(user_id)


        # checks if the user even has notes'
        if not all_usernotes:
            await interaction.followup.send("You dont even have notes")
            return
        

        # here we create the facts for the user to remember
        facts = await asyncio.to_thread(AI_Model.memory_battle, user_id, all_usernotes)



        # create the quiz while your at it
        quiz = await asyncio.to_thread(AI_Model.memory_quiz, user_id, facts)

        
        # save the facts into the bot
        self.memory_battles[user_id] = facts




        # now print the message for the user
        message = "🧠 **Memory Battle**\n\n"

        for number, fact in enumerate(facts, start = 1):
            message += f"{number}️⃣ {fact}\n"

        message_sent = await interaction.followup.send(message, wait=True)


        # gives the user 30 seconds then delete the previous message
        await asyncio.sleep(30)
        await message_sent.delete()
        await interaction.followup.send("⏳ Time is up! Let's test your memory.")

        # tells the user we are preparing the quiz
        await interaction.followup.send("AI Model is creating a quiz. Please wait.")
        await asyncio.sleep(3)

        # create a score for the user
        score = 0

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        
        for q in quiz:
            await interaction.followup.send(q["question"])

            try:
                answer = await self.bot.wait_for("message", check = check, timeout=30)

                user_answer = answer.content
                correct_answer = q["answer"]

                # compare them
                if user_answer.lower() == correct_answer.lower():
                    score += 1
                    await interaction.followup.send("✅ Correct!")
                else:
                    await interaction.followup.send(f"❌ Wrong! The answer was {correct_answer}")
            except asyncio.TimeoutError:
                await interaction.followup.send("⏰ Time ran out!")
                break
        await interaction.followup.send(f"You have scored {score}/{len(quiz)}")


        # here we do funny gif
        if score == 0:
            await asyncio.sleep(1)
            await interaction.followup.send("https://klipy.com/gifs/lock-in-twin")
        elif score == 1:
            await asyncio.sleep(1)
            await interaction.followup.send("https://klipy.com/gifs/bruh-sad-1")
        elif score == 2:
            await asyncio.sleep(1)
            await interaction.followup.send("https://klipy.com/gifs/soso-4")
        elif score == 3:
            await asyncio.sleep(1)
            await interaction.followup.send("https://klipy.com/gifs/pikanod")
        elif score == 4:
            await asyncio.sleep(1)
            await interaction.followup.send("https://klipy.com/gifs/ted-lasso-potential")
        elif score == 5:
            await asyncio.sleep(1)
            await interaction.followup.send("https://klipy.com/gifs/keep-going-75")
        











                                            


















   

           
  


  


        
        








        
        

        







            


        
         





 
         
        















        



        


            
                                                    










   



            



            








 



        

        



        
        



    



        
            
            


            
           



        



            
        
            


                    

        
    


        
            
     

            
       

         
        
        

            

          


    
        
        

                





            


        




         


        
            





      
        
                
                

         

                    
                    
        
    
            
            
        
        



            
                

            
        
# the steup at the bottom to link the cog
async def setup(bot):
     await bot.add_cog(revision(bot))
     