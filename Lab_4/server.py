import Pyro4
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS teams (
                    team_id INTEGER PRIMARY KEY,
                    team_name TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                    player_id INTEGER PRIMARY KEY,
                    player_name TEXT,
                    team_id INTEGER,
                    FOREIGN KEY(team_id) REFERENCES teams(team_id))''')
conn.commit()

@Pyro4.expose
class Server:
    def add_team(self, team_name):
        cursor.execute('INSERT INTO teams (team_name) VALUES (?)', (team_name,))
        conn.commit()
        return f"Team '{team_name}' added successfully."

    def add_player(self, player_name, team_id):
        cursor.execute('INSERT INTO players (player_name, team_id) VALUES (?, ?)', (player_name, team_id))
        conn.commit()
        return f"Player '{player_name}' added to team {team_id} successfully."

    def list_teams(self):
        cursor.execute('SELECT * FROM teams')
        return cursor.fetchall()

    def list_players_in_team(self, team_id):
        cursor.execute('SELECT * FROM players WHERE team_id=?', (team_id,))
        return cursor.fetchall()

    def update_player_name(self, player_id, new_name):
        cursor.execute('UPDATE players SET player_name=? WHERE player_id=?', (new_name, player_id))
        conn.commit()
        return f"Player ID '{player_id}' renamed to '{new_name}'."

    def delete_player(self, player_id):
        cursor.execute('DELETE FROM players WHERE player_id=?', (player_id,))
        conn.commit()
        return f"Player ID '{player_id}' deleted."

    def delete_team(self, team_id):
        cursor.execute('DELETE FROM teams WHERE team_id=?', (team_id,))
        conn.commit()
        return f"Team ID '{team_id}' deleted."


daemon = Pyro4.Daemon()
uri = daemon.register(Server)
print("URI:", uri)

ns = Pyro4.locateNS()
ns.register("example.server", uri)

print("Server is ready.")
daemon.requestLoop()
