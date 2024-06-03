import asyncio
from queue import ClientMessageQueue

async def main():
    server_queue = ClientMessageQueue('SRV.Q')

    requests = [
        'ADD_TEAM Team_1',
        'ADD_PLAYER Player_1 1',
        'LIST_TEAMS',
        'LIST_PLAYERS_IN_TEAM 1',
        'UPDATE_PLAYER_NAME 1 Player_2',
        'DELETE_PLAYER 1',
        'DELETE_TEAM 1'
    ]
    for request in requests:
        await server_queue.send(request)
        print(f'Sent request: {request}')

    client_queue = ClientMessageQueue('CL.Q')
    for _ in range(len(requests)):
        response = await client_queue.receive()
        print(f'Received response: {response}')

    await server_queue.close()
    await client_queue.close()

if __name__ == "__main__":
    asyncio.run(main())
