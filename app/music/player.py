import asyncio
from dataclasses import dataclass
from enum import StrEnum
import discord
import yt_dlp

class LoopMode(StrEnum):
    OFF = "off"
    TRACK = "track"
    QUEUE = "queue"

@dataclass(slots=True)
class Track:
    title: str
    url: str
    stream_url: str
    duration: int | None = None
    thumbnail: str | None = None
    requester_id: int | None = None

@dataclass
class GuildPlayer:
    queue: list[Track]
    current: Track | None = None
    loop: LoopMode = LoopMode.OFF
    volume: int = 70

class AudioExtractor:
    OPTIONS = {"format":"bestaudio/best","noplaylist":True,"quiet":True,"no_warnings":True}
    async def extract(self, query: str) -> Track:
        target = query if query.startswith(("http://","https://")) else f"ytsearch1:{query}"
        info = await asyncio.to_thread(self._sync, target)
        if info.get("entries"): info = next(iter(info["entries"]), None)
        if not info or not info.get("url"): raise RuntimeError("Não foi possível obter o áudio.")
        return Track(info.get("title","Faixa desconhecida"), info.get("webpage_url") or query, info["url"], info.get("duration"), info.get("thumbnail"))
    def _sync(self, target):
        with yt_dlp.YoutubeDL(self.OPTIONS) as ydl: return ydl.extract_info(target, download=False)

class PlayerManager:
    def __init__(self):
        self.players: dict[int,GuildPlayer] = {}
        self.locks: dict[int,asyncio.Lock] = {}
        self.extractor = AudioExtractor()
    def get(self, guild_id:int) -> GuildPlayer:
        return self.players.setdefault(guild_id, GuildPlayer([]))
    def lock(self, guild_id:int) -> asyncio.Lock:
        return self.locks.setdefault(guild_id, asyncio.Lock())
