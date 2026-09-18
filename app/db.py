from pathlib import Path
import aiosqlite

class Database:
    def __init__(self, path: str):
        self.path = Path(path)
        self.conn: aiosqlite.Connection | None = None

    async def connect(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = await aiosqlite.connect(self.path)
        self.conn.row_factory = aiosqlite.Row
        await self.conn.executescript("""
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS guild_settings(guild_id INTEGER PRIMARY KEY, volume INTEGER NOT NULL DEFAULT 70, language TEXT NOT NULL DEFAULT 'pt-BR');
        CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER NOT NULL, user_id INTEGER NOT NULL, title TEXT NOT NULL, url TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
        """)
        await self.conn.commit()

    async def execute(self, sql: str, params: tuple = ()):
        if not self.conn: raise RuntimeError("Banco não inicializado")
        cur = await self.conn.execute(sql, params)
        await self.conn.commit()
        return cur

    async def fetchall(self, sql: str, params: tuple = ()):
        if not self.conn: raise RuntimeError("Banco não inicializado")
        cur = await self.conn.execute(sql, params)
        return await cur.fetchall()

    async def close(self):
        if self.conn: await self.conn.close()
