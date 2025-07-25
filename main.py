import discord
from discord import ui, app_commands
from datetime import datetime
import json
from config import token, guild_id, role_id

# Initialize bot
intents = discord.Intents.all()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Modal definition for Minecraft registration
class MyModal(ui.Modal):
    def __init__(self):
        super().__init__(title='Minecraft Registration')

        self.username = ui.TextInput(
            label='Minecraft Username',
            style=discord.TextStyle.short,
            placeholder='Your Minecraft Username',
            required=True,
            min_length=3,
            max_length=20
        )

        self.email = ui.TextInput(
            label='Minecraft Email',
            style=discord.TextStyle.short,
            placeholder='Your Minecraft Email',
            required=True,
            min_length=8,
            max_length=50
        )

        self.add_item(self.username)
        self.add_item(self.email)

    async def on_submit(self, interaction: discord.Interaction):
        username = self.username.value
        email = self.email.value

        submission = {
            'username': username,
            'email': email
        }

        try:
            with open('registrations.json', 'r') as f:
                submissions = json.load(f)
        except FileNotFoundError:
            submissions = {}

        submissions[username] = submission

        with open('registrations.json', 'w') as f:
            json.dump(submissions, f, indent=4)

        embed = discord.Embed(
            title=self.title,
            description="Registration successful!",
            timestamp=datetime.now(),
            color=discord.Colour.blue()
        )
        embed.add_field(name='Minecraft Email', value=email)
        embed.add_field(name='Minecraft Username', value=username)
        embed.set_author(name=str(interaction.user), icon_url=interaction.user.avatar.url if interaction.user.avatar else None)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        role = interaction.guild.get_role(role_id)
        if role:
            try:
                await interaction.user.add_roles(role)
            except discord.Forbidden:
                await interaction.followup.send("I don't have permission to add roles.", ephemeral=True)


# Register slash command for modal
@tree.command(guild=discord.Object(id=guild_id), name='modal', description='Open the Minecraft Registration Modal')
async def modal(interaction: discord.Interaction):
    await interaction.response.send_modal(MyModal())

# Register slash command with a button that opens the modal
@tree.command(guild=discord.Object(id=guild_id), name='verify', description='Verify and register your Minecraft account')
async def verify(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Verify Your Minecraft Account",
        description="Click the button below to register your Minecraft account.",
        color=discord.Color.blurple()
    )

    view = ui.View()

    async def button_callback(interaction: discord.Interaction):
        await interaction.response.send_modal(MyModal())

    button = ui.Button(label="Register", style=discord.ButtonStyle.primary)
    button.callback = button_callback
    view.add_item(button)

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


# Sync commands once on ready
@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id))
    print(f"Bot logged in as {bot.user} and commands synced.")


bot.run(token)
