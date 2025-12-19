# SYSTEM PACKAGES
import os
import subprocess
import logging

# EXTERNAL PACKAGES
import discord
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

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged On As {self.user}...')
        print("-----")

intents = discord.Intents.all()
intents.message_content = True

client = Client(intents=intents)
client.run(TOKEN)
