import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")
    await bot.tree.sync()  

@bot.tree.command(name="ping", description="Testa se o bot está vivo")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! 🏓")

@bot.tree.command(name="clima", description="Consulta o clima atual de uma cidade")
async def clima(interaction: discord.Interaction, cidade: str):
    await interaction.response.defer()  # avisa o Discord que a resposta vai demorar um pouco

    async with aiohttp.ClientSession() as session:
        url = f"https://wttr.in/{cidade}?format=%C+%t+(sensação:+%f)"
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    dado = await resp.text()
                    embed = discord.Embed(
                        title=f"Clima em {cidade.title()}",
                        description=dado,
                        color=discord.Color.blue()
                    )
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send("Não consegui encontrar essa cidade 😕")
        except Exception as e:
            await interaction.followup.send("Erro ao buscar o clima. Tenta de novo em instantes.")

bot.run(TOKEN)