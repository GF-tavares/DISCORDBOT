import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


class MeuBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    
    async def setup_hook(self):
       
        await self.load_extension("cogs.utilidades")
        await self.load_extension("cogs.musica") 
        
        
        await self.tree.sync()

    async def on_ready(self):
        print(f"Bot online como {self.user}")


bot = MeuBot()
bot.run(TOKEN)