import asyncio

class ServerQueue:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.queue = asyncio.Queue()

    async def receive(self):
        return await self.queue.get()

    async def send(self, message):
        await self.queue.put(message)

class ClientQueue:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.queue = asyncio.Queue()

    async def receive(self):
        return await self.queue.get()

    async def send(self, message):
        await self.queue.put(message)
