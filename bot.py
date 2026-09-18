from app.bot import create_bot
from app.config import get_settings

if __name__ == "__main__":
    create_bot().run(get_settings().discord_token)
