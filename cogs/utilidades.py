import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Testa se o bot está vivo")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong! 🏓")

    @app_commands.command(name="clima", description="Consulta o clima atual de uma cidade")
    async def clima(self, interaction: discord.Interaction, cidade: str):
        await interaction.response.defer()

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

async def setup(bot):
    await bot.add_cog(Utilidades(bot))