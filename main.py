import discord
from discord.ext import commands
from discord import app_commands
import os  # Import os for environment variables
from keep_alive import keep_alive

# ✅ Securely get the bot token and Guild ID from Replit Secrets
TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=GUILD_ID)  # ✅ Use the secure Guild ID
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.lower().startswith('hello'):
            await message.reply(f'Hi there {message.author.mention}!')

        if message.content.lower().startswith('ping'):
            await message.reply(f'pong')

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

# ✅ Use the stored Guild ID in commands
@client.tree.command(name="hello", description="Say hello to the bot!", guild=discord.Object(id=GUILD_ID))
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")

@client.tree.command(name="printer", description="I will print whatever you give me!", guild=discord.Object(id=GUILD_ID))
async def sayPrinter(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

keep_alive()
# ✅ Run the bot using the secure token
client.run(TOKEN)
