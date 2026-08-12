import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp 
import yt_dlp
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

# CONFIGURAÇÕES DO YT_DLP PARA EXTRAIR AUDIO DO YOUTUBE
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'extract_flat': False,
    'force_generic_extractor': False
}

# CONFIGURAÇÕES DO FFMPEG PARA STREAMING DE ÁUDIO
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

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

            
# --- COMANDOS DE MÚSICA ---

@bot.tree.command(name="play", description="Toca uma música do YouTube (URL ou Nome)")
async def play(interaction: discord.Interaction, busca: str):
    if not interaction.user.voice:
        await interaction.response.send_message("⚠️ Você precisa estar em um canal de voz para tocar música!", ephemeral=True)
        return

    await interaction.response.defer()

    voice_channel = interaction.user.voice.channel
    voice_client = interaction.guild.voice_client

    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_client.channel != voice_channel:
        await voice_client.move_to(voice_channel)

    with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{busca}" if not busca.startswith("http") else busca, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            
            audio_url = info['url']
            titulo = info.get('title', 'Música sem título')
        except Exception as e:
            await interaction.followup.send("❌ Ocorreu um erro ao buscar a música.")
            print(f"Erro no yt-dlp: {e}")
            return

    if voice_client.is_playing() or voice_client.is_paused():
        voice_client.stop()
        await asyncio.sleep(1)

    source = discord.FFmpegPCMAudio(audio_url, executable="./ffmpeg.exe", **FFMPEG_OPTIONS)
    voice_client.play(source)

    await interaction.followup.send(f"🎵 **Tocando agora:** `{titulo}`")


@bot.tree.command(name="leave", description="Desconecta o bot do canal de voz")
async def leave(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await interaction.response.send_message("👋 Desconectado do canal de voz!")
    else:
        await interaction.response.send_message("Eu não estou em nenhum canal de voz.", ephemeral=True)

bot.run(TOKEN)