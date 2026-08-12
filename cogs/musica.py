import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio

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

# CONFIGURAÇÕES DO FFMPEG PARA STREAMING DE ÁUDIO MAIS ESTÁVEL
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M',
    'options': '-vn -sn -dn' 
}

class Musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play", description="Toca uma música do YouTube (URL ou Nome)")
    async def play(self, interaction: discord.Interaction, busca: str):
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

    @app_commands.command(name="stop", description="Para a música atual")
    async def stop(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
            voice_client.stop()
            await interaction.response.send_message("⏹️ Música interrompida!")
        else:
            await interaction.response.send_message("Nenhuma música tocando no momento.", ephemeral=True)
            
    @app_commands.command(name="leave", description="Desconecta o bot do canal de voz")
    async def leave(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client:
            await voice_client.disconnect()
            await interaction.response.send_message("👋 Desconectado do canal de voz!")
        else:
            await interaction.response.send_message("Eu não estou em nenhum canal de voz.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Musica(bot))