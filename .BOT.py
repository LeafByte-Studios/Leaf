# SYSTEM PACKAGES
import os
from pydoc import cli
import subprocess
import logging

# EXTERNAL PACKAGES
import discord
from discord import app_commands
from dotenv import load_dotenv

# CLEAR TERMINAL
def clear_terminal():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


load_dotenv()

# LOAD VARIABLES
# TOKEN
TOKEN = os.getenv("TOKEN")

# INVITE
INVITE = os.getenv("INVITE")

# PRINT VARIABLES...
print("-----")
print("The .env Has Loaded...")
print("-----")
print(f" TOKEN: {TOKEN}")
print(f" INVITE: {INVITE}")
print("-----")

# Set the Discord logger to WARNING
logging.getLogger('discord').setLevel(logging.WARNING)
logging.getLogger('discord.gateway').setLevel(logging.WARNING)
logging.getLogger('discord.client').setLevel(logging.WARNING)

GUILD_ID_NUM = 1446806402877231196

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged On As {self.user}...')
        client.tree.clear_commands(guild=None)
        synced_commands = await client.tree.sync(guild=discord.Object(id=GUILD_ID_NUM))
        print(f"Synced {len(synced_commands)} Commands.")
        for command in synced_commands:
            print(f'- {command.name}')
        print("-----")




intents = discord.Intents.all()
intents.message_content = True

client = Client(intents=intents)
client.tree = app_commands.CommandTree(client)



@client.tree.command(name="echo", description="Echoes A Message.", guild=discord.Object(id=GUILD_ID_NUM))
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"{interaction.user.mention}  |  {message}")



client.run(TOKEN)
