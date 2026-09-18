# Discord Music Bot

Bot de música modular e assíncrono para Discord usando discord.py 2.7+, yt-dlp, FFmpeg, SQLite e Pydantic.

## Recursos

- Slash commands globais
- Pesquisa por nome com yt-dlp
- Fila independente por servidor
- Pause, resume, skip, stop, queue e nowplaying
- Volume, shuffle e loop off/track/queue
- SQLite assíncrono com WAL
- Health check
- Docker, GitHub Actions e Termux
- Base preparada para PostgreSQL, Redis, métricas e Lavalink
- Comando forgetme para remover histórico

## Instalação

Instale Python 3.12+, FFmpeg e Git. Copie .env.example para .env, preencha DISCORD_TOKEN e execute:

python -m pip install -e .
python bot.py

## Termux

pkg update
pkg install python ffmpeg git
python -m pip install -U pip
python -m pip install -e .
python bot.py

## Comandos

/play /pause /resume /skip /stop /queue /nowplaying /volume /shuffle /loop /join /leave /settings /health /forgetme

## Privacidade

O bot deve armazenar somente o mínimo necessário. O operador deve respeitar LGPD, direitos autorais e os termos das plataformas usadas como fonte. O projeto transmite áudio em tempo real e não foi projetado para armazenamento permanente de mídia.
