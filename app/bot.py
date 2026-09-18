import logging
import discord
from discord.ext import commands
from .config import get_settings
from .db import Database
from .music.player import PlayerManager

class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.none()
        intents.guilds = True
        intents.voice_states = True
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)
        self.settings = get_settings()
        self.db = Database(self.settings.database_path)
        self.players = PlayerManager()
    async def setup_hook(self):
        await self.db.connect()
        await self.load_extension("app.cogs.music")
        await self.load_extension("app.cogs.settings")
        synced = await self.tree.sync()
        logging.getLogger("musicbot").info("Comandos globais sincronizados: %s", len(synced))
    async def close(self):
        await self.db.close()
        await super().close()
    async def on_ready(self):
        logging.getLogger("musicbot").info("Online como %s | servidores=%s", self.user, len(self.guilds))

def create_bot():
    logging.basicConfig(level=getattr(logging,get_settings().log_level.upper(),logging.INFO), format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    return MusicBot()
