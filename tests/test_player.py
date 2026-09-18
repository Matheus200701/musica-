from app.music.player import GuildPlayer, LoopMode

def test_player_defaults():
    player = GuildPlayer([])
    assert player.current is None
    assert player.loop == LoopMode.OFF
    assert player.volume == 70

def test_queue_isolated():
    a = GuildPlayer([])
    b = GuildPlayer([])
    a.queue.append("x")
    assert b.queue == []
