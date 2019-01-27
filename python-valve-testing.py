import valve.source.a2s

serverDetails=("37.10.127.157", 5757)

server = valve.source.a2s.ServerQuerier(serverDetails,timeout=3)

try:
    info = server.get_info()
    players = server.get_players()
    print(players)
except Exception:
    print("Failed")
    exit(1)
