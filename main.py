import discord
from discord.ext import commands

# --- Config setup --- #
import json

with open('config.json') as f:
    config = json.load(f)

token = config.get('bot_token')
logs_channel_id = config.get('logs_channel_id')

prefix = config.get('prefix')
command_name = config.get('command_name')

give_role = config.get('give_role')
role_name = config.get('role_name')

# --- Bot Start --- #
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.command()
async def verify(ctx):
    # Create an embed
    embed = discord.Embed(
        title="Link a Minecraft Account!",
        description="To verify, please link a new Minecraft account by pressing the button below.",
        color=0x00ff00  # You can customize the color
    )
    embed.add_field(name="Why am I not verified yet?", value="1. You entered the incorrect email linked to the provided username.\n2. You have entered the wrong email or username of an alt account. We have an extensive database of alt accounts to prevent cheaters from joining. We hereby enforce our Rules and Policies: [Discord Invite Link](https://discord.gg/6bhn4Q9Y).\n3. The bot is experiencing heavy load or is currently down.")
    embed.add_field(name="After linking your account, you can apply for the guild SMP in", value="Your desired location for applying for the guild SMP.")

    # Create a button
    button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Link Minecraft Account", custom_id="minecraft_verification")

    # Create a view and add the button to it
    view = discord.ui.View()
    view.add_item(button)

    # Send the embed with the view containing the button
    await ctx.send(embed=embed, view=view)

@bot.event
async def on_button_click(interaction):
    print(interaction.custom_id)
    if interaction.custom_id == "minecraft_verification":
        await interaction.message.channel.send("Please type your Minecraft username here.")

# --- Bot run --- #
bot.run(token)
