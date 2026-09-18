import discord
from discord import app_commands
from discord.ext import commands

class Settings(commands.Cog):
    def __init__(self,bot): self.bot=bot
    @app_commands.command(name="health",description="Verifica a saúde do bot.")
    async def health(self,interaction):
        await self.bot.db.fetchall("SELECT 1")
        await interaction.response.send_message(f"🟢 Gateway: {self.bot.latency*1000:.0f}ms\n🟢 Banco: OK\n🟢 Servidores: {len(self.bot.guilds)}")
    @app_commands.command(name="settings",description="Mostra as configurações do servidor.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def settings(self,interaction):
        rows=await self.bot.db.fetchall("SELECT volume,language FROM guild_settings WHERE guild_id=?",(interaction.guild.id,))
        if not rows:
            await self.bot.db.execute("INSERT OR IGNORE INTO guild_settings(guild_id,volume) VALUES (?,?)",(interaction.guild.id,self.bot.settings.default_volume))
            rows=await self.bot.db.fetchall("SELECT volume,language FROM guild_settings WHERE guild_id=?",(interaction.guild.id,))
        r=rows[0]; await interaction.response.send_message(f"⚙️ Volume padrão: {r['volume']}% | Idioma: {r['language']}")
    @app_commands.command(name="forgetme",description="Remove seu histórico armazenado pelo bot.")
    async def forgetme(self,interaction):
        await self.bot.db.execute("DELETE FROM history WHERE user_id=?",(interaction.user.id,))
        await interaction.response.send_message("🗑️ Seu histórico foi removido.",ephemeral=True)
async def setup(bot): await bot.add_cog(Settings(bot))
