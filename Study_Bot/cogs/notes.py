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

class notescog(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @app_commands.command(name="addnotes", description="Take notes and save them to the database")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def notes(self, interaction: discord.Interaction, notes: str,):

        # converts the userid
        user_id = interaction.user.id

        
        all_catogries = db.call_category(interaction.user.id)

        if not all_catogries:
            await interaction.response.send_message("You do not have catoreiges. Please use the categories command to put notes in")
            return 
        
        
        # tells the user we are saving the notes
        await asyncio.sleep(1)
        await interaction.response.send_message("Saving your note...")
        await asyncio.sleep(2)

        
        
        # get all notes
        all_categories = db.call_category(user_id)
        print(all_categories)

        options = []

        for category1 in all_categories:
            options.append(
                discord.SelectOption(
                    label = category1[0]
                )
            )

        # DropDown Men Select
        class CategoryDropDownSelect(discord.ui.Select):
            def __init__(self, options):
                super().__init__(
                    placeholder = "Choose the Category",
                    options = options
                )

            async def callback(self, interaction):
                category = self.values[0]
                category = category.strip().title()

                

                db.save_notes(user_id, notes, category)
                print("category is saved")
                print(category)

                await interaction.response.send_message(f"You chose {category}")

        # DropDownMenu View
        class CategoryDropDownView(discord.ui.View):
            def __init__(self, options):
                super().__init__()
                self.add_item(CategoryDropDownSelect(options))

        # create the actually view now
        view = CategoryDropDownView(options)

        # create the output for the actual drop down menu
        await interaction.followup.send("Choose a category", view=view)



    @app_commands.command(name="showcase", description="This will be a showcase of your notes")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def showcase(self, interaction: discord.Interaction):

        # tells discord to wait
        await interaction.response.defer()

        # convert the user id
        user_id = interaction.user.id

        all_categories = db.call_category(interaction.user.id)
        print(all_categories)

        options = []

        for category2 in all_categories:
            options.append(
                discord.SelectOption(
                    label = category2[0]
                )
            )

        # DropDown Men Select
        class CategoryDropDownSelect(discord.ui.Select):
            def __init__(self, options):
                super().__init__(
                    placeholder = "Choose the Category",
                    options = options
                )

            async def callback(self, interaction):
                category = self.values[0]
                category = category.strip().title()

                

                await interaction.response.send_message(f"You chose {category}")

        # DropDownMenu View
        class CategoryDropDownView(discord.ui.View):
            def __init__(self, options):
                super().__init__()
                self.add_item(CategoryDropDownSelect(options))

        # create the actually view now
        view = CategoryDropDownView(options)

        # create the output for the actual drop down menu
        await interaction.followup.send("Choose a category", view=view)


        # once we get the chosen category we showcase whats in it
        all_notes = db.get_notes(user_id)
        all_cateogries = db.call_category(user_id)



        



        





   

    @app_commands.command(name="deletenotes", description="Deletes the notes you have saved")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def deletenotes(self, interaction: discord.Interaction):

        # checks if the user has any notes
        notes = db.get_notes(interaction.user.id)

        if not notes:
            await interaction.response.send_message("You don't have any notes saved!")
            return

        # ask the user would they like to delete all notes or a specific one
        await interaction.response.send_message("Would you like to delete all notes or a specific one 1 is all notes and 2 is a specific note?")

        # waits for the user to send the notes
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)

            # checks if the user wants to delete all notes or a specific one
            if msg.content == "1":
                # tells the user are they sure about deleting all notes
                await interaction.followup.send("Are you sure you want to delete all notes? (yes/no)")
                msg2 = await self.bot.wait_for('message', check=check, timeout=30.0)
                if msg2.content == "yes":
                    db.delete_notes(interaction.user.id)
                    await interaction.followup.send("All notes deleted successfully!")
                    return
                else:
                    await interaction.followup.send("Cancelled.")
                    return
            elif msg.content == "2":
                # tells the user to enter the number of the note they want to delete
                await interaction.followup.send("Please enter the number of the note you want to delete.")
                for note in notes:
                    await interaction.followup.send(f"{note[0]}. {note[2]}")

                # waits for the user to send the number of the note they want to edit
                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    msg3 = await self.bot.wait_for('message', check=check, timeout=30.0)

                    # checks if they even enter a number
                    if not msg3.content.isdigit():
                        await interaction.followup.send("Please enter a valid number.")
                        return

                    # checks if the id is within the database
                    valid_ids = [note[0] for note in notes]
                    if int(msg3.content) not in valid_ids:
                        await interaction.followup.send("Please enter a valid ID.")
                        return

                    # deletes the note
                    db.delete_note(interaction.user.id, int(msg3.content))
                    await interaction.followup.send("Note deleted successfully!")
                    return
                except asyncio.TimeoutError:
                    await interaction.followup.send("You took too long to respond. Cancelled.")
        except Exception as e:
            print(e)
                
         
    @app_commands.command(name="editnote", description="Edits the notes you have saved")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def editnote(self, interaction: discord.Interaction):

        # checks if the user has any notes
        notes = db.get_notes(interaction.user.id)
        if not notes:
            await interaction.send_message("You don't have any notes saved!")
            return

        # new note
        new_note = None
        
        # ask the user which note they want to edit
        await interaction.response.send_message("Please enter the ID of the note you want to edit.")
        for note in notes:
            await interaction.followup.send(f"{note[0]}. {note[2]}")

        # waits for the user to send the number of the note they want to edit
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)

            # checks if they even enter a number
            if not msg.content.isdigit():
                await interaction.followup.send("Please enter a valid number.")
                return

            # checks if the id is within the database
            valid_ids = [note[0] for note in notes]
            if int(msg.content) not in valid_ids:
                await interaction.followup.send("Please enter a valid ID.")
                return

            # asks the user what they want to change the note to
            await interaction.followup.send("Please enter the new note.")
            
            # waits for the user to send the new note
            msg2 = await self.bot.wait_for('message', check=check, timeout=30.0)


            # updates the note
            db.update_note(interaction.user.id, int(msg.content), msg2.content)
            await interaction.followup.send("Note updated successfully!")
        except asyncio.TimeoutError:
            await interaction.followup.send("You took too long to respond. Cancelled.")

    @app_commands.command(name="searchnotes", description="Searches for a note in your notes")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def searchnotes(self, interaction: discord.Interaction, search_term: str):

        # checks if the user has any notes
        notes = db.get_notes(interaction.user.id)
        if not notes:
            await interaction.response.send_message("You don't have any notes saved!")
            return

        # searches for the note
        db.search_notes(interaction.user.id, search_term)
        await interaction.response.send_message(f"Searching for {search_term}...")

        # checks if the note exists
        if not db.search_notes(interaction.user.id, search_term):
            await interaction.followup.send("No notes found!")
            return

        # shows the note
        await interaction.followup.send(f"Found {len(db.search_notes(interaction.user.id, search_term))} notes!")
        for note in db.search_notes(interaction.user.id, search_term):
            await interaction.followup.send(f"{note[0]}. {note[2]}")
        return

    @app_commands.command(name="latestnotes", description="Shows the last 5 notes you have saved")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def latestnotes(self, interaction: discord.Interaction):

        # checks if the user has any notes
        notes = db.get_notes(interaction.user.id)
        if not notes:
            await interaction.response.send_message("You don't have any notes saved!")
            return

        # also checks if the user has less than 5 notes
        if db.latest_notes(interaction.user.id):
            await interaction.response.send_message("You don't have enough notes to show the latest 5!")
            return
            
        
        # shows the latest note
        await interaction.response.send_message("Showing your latest note...")
        await asyncio.sleep(2)

        # gets the last 5 notes from the database
        latest_note = db.get_notes(interaction.user.id)[-5:]
        for note in latest_note:
            await interaction.followup.send(f"{note[0]}. {note[2]}")
        return
    
    @app_commands.command(name="pinnote", description="Pin an important note to the top of your notes.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def shownotes(self, interaction: discord.Interaction):

        # shows the notes the user has saved
        await interaction.response.send_message("Showing your notes...")

        # gets the notes from the database
        all_notes = db.get_notes(interaction.user.id)

        # checks if the user has any notes
        if not all_notes:
            await interaction.followup.send("You don't have any notes saved!")
            return

        # loops through the notes showcasing each one
        msg = ""
        for i, note in enumerate(all_notes, start=1):
            msg += f"{i}. {note[2]}\n"

        await interaction.followup.send(f"{msg}")

        
        # tells the user which note they would like to pin
        await interaction.followup.send("Which note would you like to pin")

    @app_commands.command(name="addacategory", description="Pin an important note to the top of your notes.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def shownotes(self, interaction: discord.Interaction, category: str):

        # defer due to thinking
        await interaction.response.defer()


        all_catogries = db.call_category(interaction.user.id)
        await interaction.followup.send("Saving your Cateogry..")

        # checks if the category is already within the database
        if category in all_catogries:
            await interaction.response.followup.send("You already have this category. Please try again")
            return
        
        # saves the category within the category table
        success = db.add_category(interaction.user.id, category)
        if success:
            await interaction.followup.send("✅ Category saved!")
            print(f"User ID: {interaction.user.id}, Category: {category}")
        else:
            await interaction.followup.send("❌ Category failed!")
            return


     








    
            
    



        
            
            


            
           



        



            
        
            


                    

        
    


        
            
     

            
       

         
        
        

            

          


    
        
        

                





            


        




         


        
            





      
        
                
                

         

                    
                    
        
    
            
            
        
        



            
                

            
        
# the steup at the bottom to link the cog
async def setup(bot):
     await bot.add_cog(notescog(bot))
     