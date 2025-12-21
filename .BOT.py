# SYSTEM PACKAGES
import os
import logging
import string
from datetime import timedelta


# EXTERNAL PACKAGES
import toml
import discord
from discord import app_commands
from dotenv import load_dotenv

# CLEAR TERMINAL
def clear_terminal():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def check_section_exists(file_path, section_name):
    if not os.path.exists(file_path):
        print(f"Error: The File '{file_path}' Was Not Found.")
        return False

    # Load existing TOML (TEXT MODE)
    with open(".config.toml", "r", encoding="utf-8") as f:
        data = toml.load(f)

    # Check if the section name is a key in the loaded dictionary
    if section_name in data:
        return True
    else:
        return False

def parse_duration(duration: str) -> int:
    units = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
    }

    amount = int(duration[:-1])
    unit = duration[-1]

    if unit not in units:
        raise ValueError("Invalid time format")

    return amount * units[unit]


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
print(" TOKEN: MT*****Te2RA")
print(f" INVITE: {INVITE}")
print("-----")

# Set the Discord logger to WARNING
logging.getLogger('discord').setLevel(logging.WARNING)
logging.getLogger('discord.gateway').setLevel(logging.WARNING)
logging.getLogger('discord.client').setLevel(logging.WARNING)

GUILD_ID_NUM = 1446806402877231196
global mod_log_channel
mod_log_channel = "null"

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged On As {self.user}...')
        print("-----")

        client.tree.clear_commands(guild=None)
        synced_commands = await client.tree.sync(guild=discord.Object(id=GUILD_ID_NUM))
        print(f"Synced {len(synced_commands)} Commands.")
        for command in synced_commands:
            print(f'- {command.name}')
        print("-----")

        for guild in client.guilds:
            print(f"Guild name: {guild.name} | Guild ID: {guild.id}")
        print("-----")

class ModLogChannelSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.select(
        cls=discord.ui.ChannelSelect,
        placeholder="Select A Channel...",
        channel_types=[discord.ChannelType.text, discord.ChannelType.voice],
        min_values=1,
        max_values=1,
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.ChannelSelect):
        selected_channel = select.values[0]

        guild = interaction.guild
        guild_id = selected_channel.guild.id

        # Load existing TOML (TEXT MODE)
        with open(".config.toml", "r", encoding="utf-8") as f:
            data = toml.load(f)

        # IMPORTANT: TOML keys must be strings
        data[f'{guild_id}']['mod_log_channel'] = f'{selected_channel.id}'

        # Write back to file (TEXT MODE)
        with open(".config.toml", "w", encoding="utf-8") as f:
            toml.dump(data, f)

        mod_log_channel = selected_channel

        await interaction.message.delete()
        await interaction.response.send_message(f"{str.upper(guild.name)}  |  MOD LOG LOCATION  |  {mod_log_channel.mention}")

        channel = client.get_channel(mod_log_channel.id)
        if channel:
            await channel.send(f'{str.upper(guild.name)}  |  MOD LOG LOCATION  |  {interaction.user.mention}')


class ModLogConfirmView(discord.ui.View):
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success)
    async def button_callback_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(view=ModLogChannelSelectView())
        await interaction.message.delete()

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def button_callback_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()


intents = discord.Intents.all()
intents.message_content = True

client = Client(intents=intents)
client.tree = app_commands.CommandTree(client)

@client.tree.command(name="echo", description="Echoes A Message.", guild=discord.Object(id=GUILD_ID_NUM))
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"{interaction.user.mention}  |  {message}")

@client.tree.command(name="ping", description="Pings The Bot.", guild=discord.Object(id=GUILD_ID_NUM))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"PONG   |   {round(client.latency * 1000)}ms")


@client.tree.command(name="creator_info", description="Displays Information About The Bot's Creator.")
async def creator_info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Bot Creator Information",
        description="This Bot Was Created By [LeafByte Studios](https://leafbyte-studios.github.io/WebSite/index.html).",
        color=discord.Color.from_rgb(221, 62, 56)
    )
    embed.thumbnail(url="/.Images/LeafByteLogo.png")

    await interaction.response.send_message(embed=embed)

config_group = app_commands.Group(name="config", description="Configuration Commands")


@config_group.command(name="mod-logs", description="Set Mod Logs Channel.")
@app_commands.checks.has_permissions(manage_guild=True)
async def mod_logs(interaction: discord.Interaction, channel: discord.TextChannel):
    channel = channel
    guild = interaction.guild

    channel_id = channel.id
    guild_id = channel.guild.id

    if not check_section_exists(".config.toml", str(guild_id)):

        # Load existing TOML (TEXT MODE)
        with open(".config.toml", "r", encoding="utf-8") as f:
            data = toml.load(f)

        # IMPORTANT: TOML keys must be strings
        data[str(guild_id)] = {
            "mod_log_channel": channel_id,
        }

        # Write back to file (TEXT MODE)
        with open(".config.toml", "w", encoding="utf-8") as f:
            toml.dump(data, f)

        mod_log_channel = channel

        await interaction.response.send_message(f"{str.upper(guild.name)}  |  MOD LOG LOCATION  |  {mod_log_channel.mention}")

        channel = client.get_channel(mod_log_channel.id)
        if channel:
            await channel.send(f'{str.upper(guild.name)}  |  MOD LOG LOCATION  |  {interaction.user.mention}')
    else:
        # Load existing TOML (TEXT MODE)
        with open(".config.toml", "r", encoding="utf-8") as f:
            data = toml.load(f)

        channel_id_string = data[str(guild_id)]["mod_log_channel"]

        # Convert the string ID to an integer
        channel_id_int = int(channel_id_string)

        # Get the channel object
        mod_log_channel = client.get_channel(channel_id_int)


        await interaction.response.send_message(f"{str.upper(guild.name)}  |  MOD LOG LOCATION  |  {mod_log_channel.mention}")
        await interaction.followup.send("Do You Want To Change?", view=ModLogConfirmView())


mod_group = app_commands.Group(name="mod", description="Moderation Commands")


@mod_group.command(name="timeout", description="Timeout A Member.")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(
    interaction: discord.Interaction,
    user: discord.Member,
    duration: str,
    reason: discord.Optional[str] = "No Reason Provided."
):
    seconds = parse_duration(duration)

    embed = discord.Embed(
        title="Timeout",
        color=discord.Color.red()
    )

    _str = interaction.user.name
    user_name = _str.title()

    embed.set_footer(text=f"{user_name}", icon_url=interaction.user.avatar.url)
    embed.add_field(name="_ _", value="_ _", inline=False)
    embed.add_field(name="User", value=user.mention, inline=False)
    embed.add_field(name="Duration", value=duration, inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.add_field(name="_ _", value="_ _", inline=False)

    await user.send(embed=embed)

    await user.timeout(
        timedelta(seconds=seconds),
        reason=f"{reason}"
    )

    await interaction.response.send_message(
        f"{user.mention} Has Been Timed Out For {duration}.",
        ephemeral=True
    )



    # Load existing TOML (TEXT MODE)
    with open(".config.toml", "r", encoding="utf-8") as f:
        data = toml.load(f)

    guild_id = interaction.guild.id

    channel_id_string = data[str(guild_id)]["mod_log_channel"]

    # Convert the string ID to an integer
    channel_id_int = int(channel_id_string)

    # Get the channel object
    mod_log_channel = client.get_channel(channel_id_int)

    channel = client.get_channel(mod_log_channel.id)

    if channel:
        await channel.send(embed=embed)


# ------------------- KICK COMMAND -------------------
@mod_group.command(name="kick", description="Kick A Member.")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(
    interaction: discord.Interaction,
    user: discord.Member,
    reason: discord.Optional[str] = "No Reason Provided."
):
    embed = discord.Embed(
        title="Kick",
        color=discord.Color.red()
    )

    embed.set_footer(
        text=interaction.user.name.title(),
        icon_url=interaction.user.avatar.url
    )

    embed.add_field(name="_ _", value="_ _", inline=False)
    embed.add_field(name="User", value=user.mention, inline=False)
    embed.add_field(name="Reason", value=reason.title(), inline=False)
    embed.add_field(name="_ _", value="_ _", inline=False)

    # DM first
    try:
        await user.send(embed=embed)
    except:
        print(f"Could not DM {user}")

    # Then kick
    try:
        await user.kick(reason=reason)
    except discord.Forbidden:
        await interaction.response.send_message(
            "I Do Not Have Permission To Kick This User.",
            ephemeral=True
        )
        return
    except discord.HTTPException as e:
        await interaction.response.send_message(
            f"Failed To Kick The User: {e}",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"{user.mention} Has Been Kicked.",
        ephemeral=True
    )

    # Log to mod channel
    try:
        with open(".config.toml", "r", encoding="utf-8") as f:
            data = toml.load(f)

        guild_id_str = str(interaction.guild.id)
        channel_id_str = data[guild_id_str]["mod_log_channel"]
        channel_id = int(channel_id_str)

        mod_log_channel = client.get_channel(channel_id)
        if mod_log_channel:
            await mod_log_channel.send(embed=embed)
    except Exception as e:
        print(f"Failed To Log Kick: {e}")


@kick.error
async def kick_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "You Don’t Have Permission To Use This Command.",
            ephemeral=True
        )
    elif isinstance(error, app_commands.TransformerError):
        await interaction.response.send_message(
            "Please Select A Valid Server Member.",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "An Unexpected Error Occurred.",
            ephemeral=True
        )
        print(f"Kick Command Error: {error}")


# ------------------- BAN COMMAND -------------------
@mod_group.command(name="ban", description="Ban A Member.")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(
    interaction: discord.Interaction,
    user: discord.Member,
    reason: discord.Optional[str] = "No Reason Provided."
):
    embed = discord.Embed(
        title="Ban",
        color=discord.Color.red()
    )

    embed.set_footer(
        text=interaction.user.name.title(),
        icon_url=interaction.user.avatar.url
    )

    embed.add_field(name="_ _", value="_ _", inline=False)
    embed.add_field(name="User", value=user.mention, inline=False)
    embed.add_field(name="Reason", value=reason.title(), inline=False)
    embed.add_field(name="_ _", value="_ _", inline=False)

    # DM first
    try:
        await user.send(embed=embed)
    except:
        print(f"Could Not DM {user}")

    # Then ban
    try:
        await user.ban(reason=reason)
    except discord.Forbidden:
        await interaction.response.send_message(
            "I Do Not Have Permission To Ban This User.",
            ephemeral=True
        )
        return
    except discord.HTTPException as e:
        await interaction.response.send_message(
            f"Failed To Ban The User: {e}",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"{user.mention} Has Been Banned.",
        ephemeral=True
    )

    # Log to mod channel
    try:
        with open(".config.toml", "r", encoding="utf-8") as f:
            data = toml.load(f)

        guild_id_str = str(interaction.guild.id)
        channel_id_str = data[guild_id_str]["mod_log_channel"]
        channel_id = int(channel_id_str)

        mod_log_channel = client.get_channel(channel_id)
        if mod_log_channel:
            await mod_log_channel.send(embed=embed)
    except Exception as e:
        print(f"Failed To Log Ban: {e}")


@ban.error
async def ban_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "You Don’t Have Permission To Use This Command.",
            ephemeral=True
        )
    elif isinstance(error, app_commands.TransformerError):
        await interaction.response.send_message(
            "Please Select A Valid Server Member.",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "An Unexpected Error Occurred.",
            ephemeral=True
        )
        print(f"Ban Command Error: {error}")


@mod_group.command(name="unban", description="Unban a user by ID.")
@app_commands.checks.has_permissions(ban_members=True)
async def unban(
    interaction: discord.Interaction,
    user_id: str,
    reason: str = "No Reason Provided."
):
    try:
        user_id = int(user_id)
    except ValueError:
        await interaction.response.send_message(
            "Please Provide A Valid Numeric User ID.",
            ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True)

    guild = interaction.guild

    # Find banned user
    try:
        ban_entry = await guild.fetch_ban(discord.Object(id=user_id))
        user = ban_entry.user
    except discord.NotFound:
        await interaction.followup.send(
            "That User Is Not Banned.",
            ephemeral=True
        )
        return
    except discord.Forbidden:
        await interaction.followup.send(
            "I Do Not Have Permission To View Bans.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="Unban",
        color=discord.Color.red()
    )
    embed.add_field(name="_ _", value="_ _", inline=False)
    embed.add_field(name="User", value=f"<@{user.id}>", inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.add_field(name="_ _", value="_ _", inline=False)
    embed.set_footer(
        text=interaction.user.name,
        icon_url=interaction.user.display_avatar.url
    )

    # Unban
    try:
        await guild.unban(user, reason=reason)
    except discord.Forbidden:
        await interaction.followup.send(
            "I Do Not Have Permission To Unban This User.",
            ephemeral=True
        )
        return

    await interaction.followup.send(
        f"**{user} Has Been Unbanned.**",
        ephemeral=True
    )
    await user.send(embed=embed)

    # Log
    try:
        with open(".config.toml", "r", encoding="utf-8") as f:
            data = toml.load(f)

        channel_id = int(data[str(guild.id)]["mod_log_channel"])
        mod_log_channel = interaction.client.get_channel(channel_id)

        if mod_log_channel:
            await mod_log_channel.send(embed=embed)

    except Exception as e:
        print(f"Failed to log unban: {e}")

    # Send DM to user
    try:
        await user.send(embed=embed)
    except discord.Forbidden:
        # User has DMs closed
        pass


client.tree.add_command(mod_group, guild=discord.Object(id=GUILD_ID_NUM))
client.tree.add_command(config_group, guild=discord.Object(id=GUILD_ID_NUM))


client.run(TOKEN)
