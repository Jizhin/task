from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_names = ["live_data_live_data"]

        # Join both room groups
        for room_name in self.room_names:
            await self.channel_layer.group_add(
                room_name ,
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, _):
        """Handles WebSocket disconnection."""
        await asyncio.gather(*(self.channel_layer.group_discard(room, self.channel_name) for room in self.room_names))

    # async def receive(self, text_data):
    #     data = json.loads(text_data)
    #     if 'message' in data and data['message']:
    #         await self.send(text_data=json.dumps({
    #             'message': data.get('message')
    #         }))

    async def send_live_data(self , event):
        print(event)
        data = event['message']
        print(data)

        await self.send(text_data=json.dumps({
            'message': data
        }))