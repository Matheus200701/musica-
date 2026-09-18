import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from app.music.player import LoopMode

class Music(commands.Cog):
    def __init__(self, bot): self.bot = bot

    async def voice(self, interaction):
        member = interaction.user
        if not isinstance(member, discord.Member) or not member.voice or not member.voice.channel:
            raise RuntimeError("Entre em um canal de voz primeiro.")
        vc = interaction.guild.voice_client
        if vc is None: vc = await member.voice.channel.connect()
        elif vc.channel != member.voice.channel: await vc.move_to(member.voice.channel)
        return vc

    async def start_next(self, guild):
        p = self.bot.players.get(guild.id); vc = guild.voice_client
        if not vc or not p.queue: p.current = None; return
        track = p.queue.pop(0); p.current = track
        source = discord.FFmpegOpusAudio(track.stream_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options=f"-vn -filter:a volume={p.volume/100}")
        def after(error): asyncio.run_coroutine_threadsafe(self.after_track(guild), self.bot.loop)
        vc.play(source, after=after)

    async def after_track(self, guild):
        p = self.bot.players.get(guild.id)
        if p.current and p.loop == LoopMode.TRACK: p.queue.insert(0,p.current)
        elif p.current and p.loop == LoopMode.QUEUE: p.queue.append(p.current)
        p.current = None
        await self.start_next(guild)

    @app_commands.command(name="play",description="Reproduz uma música ou pesquisa pelo nome.")
    @app_commands.describe(query="URL ou nome da música")
    async def play(self, interaction, query:str):
        await interaction.response.defer()
        try:
            vc = await self.voice(interaction)
            track = await self.bot.players.extractor.extract(query)
            track.requester_id = interaction.user.id
            p = self.bot.players.get(interaction.guild.id)
            async with self.bot.players.lock(interaction.guild.id): p.queue.append(track)
            if not vc.is_playing() and not vc.is_paused() and p.current is None:
                await self.start_next(interaction.guild)
                text = f"▶️ Reproduzindo **{track.title}**"
            else: text = f"➕ Adicionado: **{track.title}**"
            await interaction.followup.send(text)
        except Exception as exc: await interaction.followup.send(f"❌ {exc}")

    @app_commands.command(name="pause",description="Pausa a música.")
    async def pause(self, interaction):
        vc=interaction.guild.voice_client
        if not vc or not vc.is_playing(): return await interaction.response.send_message("❌ Nada está tocando.",ephemeral=True)
        vc.pause(); await interaction.response.send_message("⏸️ Pausado.")

    @app_commands.command(name="resume",description="Retoma a música.")
    async def resume(self, interaction):
        vc=interaction.guild.voice_client
        if not vc or not vc.is_paused(): return await interaction.response.send_message("❌ Nada está pausado.",ephemeral=True)
        vc.resume(); await interaction.response.send_message("▶️ Retomado.")

    @app_commands.command(name="skip",description="Pula a faixa atual.")
    async def skip(self, interaction):
        vc=interaction.guild.voice_client
        if not vc or not vc.is_playing(): return await interaction.response.send_message("❌ Nada está tocando.",ephemeral=True)
        vc.stop(); await interaction.response.send_message("⏭️ Pulada.")

    @app_commands.command(name="stop",description="Limpa a fila e desconecta.")
    async def stop(self, interaction):
        p=self.bot.players.get(interaction.guild.id); p.queue.clear(); p.current=None
        if interaction.guild.voice_client: await interaction.guild.voice_client.disconnect(force=True)
        await interaction.response.send_message("⏹️ Reprodução encerrada.")

    @app_commands.command(name="queue",description="Mostra a fila.")
    async def queue(self, interaction):
        p=self.bot.players.get(interaction.guild.id)
        current=f"🎵 Agora: **{p.current.title}**\n\n" if p.current else ""
        lines="\n".join(f"**{i}.** {t.title}" for i,t in enumerate(p.queue[:20],1)) or "A fila está vazia."
        await interaction.response.send_message(current+lines)

    @app_commands.command(name="nowplaying",description="Mostra a faixa atual.")
    async def nowplaying(self, interaction):
        p=self.bot.players.get(interaction.guild.id)
        if not p.current: return await interaction.response.send_message("❌ Nada está tocando.",ephemeral=True)
        e=discord.Embed(title="🎵 Tocando agora",description=p.current.title)
        if p.current.thumbnail: e.set_thumbnail(url=p.current.thumbnail)
        e.add_field(name="Volume",value=f"{p.volume}%"); e.add_field(name="Loop",value=p.loop.value)
        await interaction.response.send_message(embed=e)

    @app_commands.command(name="volume",description="Define o volume de 1 a 100.")
    async def volume(self, interaction, value:app_commands.Range[int,1,100]):
        self.bot.players.get(interaction.guild.id).volume=value
        await interaction.response.send_message(f"🔊 Volume: {value}%")

    @app_commands.command(name="shuffle",description="Embaralha a fila.")
    async def shuffle(self, interaction):
        import random; random.shuffle(self.bot.players.get(interaction.guild.id).queue)
        await interaction.response.send_message("🔀 Fila embaralhada.")

    @app_commands.command(name="loop",description="Define off, track ou queue.")
    async def loop(self, interaction, mode:str):
        try: self.bot.players.get(interaction.guild.id).loop=LoopMode(mode.lower())
        except ValueError: return await interaction.response.send_message("Use off, track ou queue.",ephemeral=True)
        await interaction.response.send_message(f"🔁 Loop: {mode.lower()}")

    @app_commands.command(name="join",description="Entra no canal de voz.")
    async def join(self, interaction): await self.voice(interaction); await interaction.response.send_message("🔊 Entrei no canal.")

    @app_commands.command(name="leave",description="Sai do canal de voz.")
    async def leave(self, interaction):
        if interaction.guild.voice_client: await interaction.guild.voice_client.disconnect(force=True)
        await interaction.response.send_message("👋 Saí do canal.")

async def setup(bot): await bot.add_cog(Music(bot))
