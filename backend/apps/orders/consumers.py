import json

from channels.generic.websocket import AsyncWebsocketConsumer

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        print(f"DEBUG: User đang kết nối là: {self.user}")
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            print(f"📡 User {self.user.username} đã kết nối WebSocket!")

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def order_status_update(self, event):
        message = event['message']
        data = event['data']

        await self.send(text_data=json.dumps({
            'type': 'ORDER_UPDATE',
            'message': message,
            'data': data
        }))