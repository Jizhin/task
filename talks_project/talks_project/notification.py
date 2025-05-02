from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs'].get('task_id')
        self.room_names = ["live_data_live_data"]
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


    async def send_comment_data(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'type': 'comment','comment': message}))
