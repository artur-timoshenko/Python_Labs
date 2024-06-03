import asyncio
from queue import ServerMessageQueue
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

async def handle_request(request):
    parts = request.split(' ')
    command = parts[0]
    if command == 'ADD_TEAM':
        team_name = parts[1]
        cursor.execute('INSERT INTO teams (team_name) VALUES (?)', (team_name,))
        conn.commit()
        return f"Team '{team_name}' added successfully."
    elif command == 'ADD_PLAYER':
        player_name = parts[1]
        team_id = int(parts[2])
        cursor.execute('INSERT INTO players (player_name, team_id) VALUES (?, ?)', (player_name, team_id))
        conn.commit()
        return f"Player '{player_name}' added to team {team_id} successfully."
    elif command == 'LIST_TEAMS':
        cursor.execute('SELECT * FROM teams')
        teams = cursor.fetchall()
        return f"Teams: {teams}"
    elif command == 'LIST_PLAYERS_IN_TEAM':
        team_id = int(parts[1])
        cursor.execute('SELECT * FROM players WHERE team_id=?', (team_id,))
        players = cursor.fetchall()
        return f"Players in team {team_id}: {players}"
    elif command == 'UPDATE_PLAYER_NAME':
        player_id = int(parts[1])
        new_name = parts[2]
        cursor.execute('UPDATE players SET player_name=? WHERE player_id=?', (new_name, player_id))
        conn.commit()
        return f"Player ID '{player_id}' renamed to '{new_name}'."
    elif command == 'DELETE_PLAYER':
        player_id = int(parts[1])
        cursor.execute('DELETE FROM players WHERE player_id=?', (player_id,))
        conn.commit()
        return f"Player ID '{player_id}' deleted."
    elif command == 'DELETE_TEAM':
        team_id = int(parts[1])
        cursor.execute('DELETE FROM teams WHERE team_id=?', (team_id,))
        conn.commit()
        return f"Team ID '{team_id}' deleted."
    else:
        return 'Invalid request'

async def main():
    server_queue = ServerMessageQueue('SRV.Q')
    client_queue = ServerMessageQueue('CL.Q')

    while True:
        request = await server_queue.receive()
        print(f'Received request: {request}')

        response = await handle_request(request)

        await client_queue.send(response)

if __name__ == "__main__":
    asyncio.run(main())
