import socket
import sqlite3

conn = sqlite3.connect('server/database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS teams (
                    team_id INTEGER PRIMARY KEY,
                    team_name TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                    player_id INTEGER PRIMARY KEY,
                    player_name TEXT,
                    team_id INTEGER,
                    FOREIGN KEY(team_id) REFERENCES teams(team_id))''')


def handle_client_request(client_socket, request):
    parts = request.split(" ")
    operation = parts[0].strip()

    if operation == "ADD_TEAM":
        team_name = parts[1].strip()
        add_team(team_name)
        client_socket.send("Team added successfully".encode())
    elif operation == "ADD_PLAYER":
        player_name = parts[1].strip()
        team_id = int(parts[2].strip())
        add_player(player_name, team_id)
        client_socket.send("Player added successfully".encode())
    else:
        client_socket.send("Invalid operation".encode())


def add_team(team_name):
    cursor.execute('INSERT INTO teams (team_name) VALUES (?)', (team_name,))
    conn.commit()
    print(f"Team '{team_name}' added successfully.")


def add_player(player_name, team_id):
    cursor.execute('INSERT INTO players (player_name, team_id) VALUES (?, ?)', (player_name, team_id))
    conn.commit()
    print(f"Player '{player_name}' added to team {team_id} successfully.")


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 12345))
        server_socket.listen()

        print("Server is running on localhost:12345")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            request = client_socket.recv(1024).decode()
            print(f"Received request from client: {request}")

            handle_client_request(client_socket, request)

            client_socket.close()


# Виклик функції для запуску сервера
if __name__ == "__main__":
    run_server()
