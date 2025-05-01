from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_names = ["live_data_live_data"]
        self.task_id = self.scope['query_string'].decode().split('=')[-1]
        if self.task_id:
            self.room_names.append(f"task_{self.task_id}")
        for room_name in self.room_names:
            await self.channel_layer.group_add(room_name, self.channel_name)

        await self.accept()

    async def disconnect(self, _):
        for room in self.room_names:
            await self.channel_layer.group_discard(room, self.channel_name)

    async def send_live_data(self, event):
        data = event['message']
        await self.send(text_data=json.dumps({'message': data}))
