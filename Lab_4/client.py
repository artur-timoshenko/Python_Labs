import Pyro4

uri = "PYRO:example.server@localhost:9090"
server = Pyro4.Proxy(uri)

server.add_team("Team 1")
server.add_player("Slava", 1)
server.list_teams()
server.list_players_in_team(1)
server.update_player_name(1, "Bebrou")
server.delete_player(1)
server.delete_team(1)
