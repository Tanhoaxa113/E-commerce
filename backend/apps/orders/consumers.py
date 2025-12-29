import json

from channels.generic.websocket import AsyncWebsocketConsumer

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Lấy user từ request (nhờ AuthMiddlewareStack)
        self.user = self.scope["user"]
        print(f"DEBUG: User đang kết nối là: {self.user}")
        if self.user.is_anonymous:
            # Chưa đăng nhập thì đuổi về
            await self.close()
        else:
            # Tạo một "Group Chat" riêng cho User này.
            # Tên group là: "user_IDCuaUser" (Ví dụ: user_10)
            self.group_name = f"user_{self.user.id}"

            # Add user vào group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            
            # Chấp nhận kết nối
            await self.accept()
            print(f"📡 User {self.user.username} đã kết nối WebSocket!")

    async def disconnect(self, close_code):
        # User thoát thì kick khỏi group
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    # Hàm này dùng để Server gửi tin nhắn xuống cho User
    async def order_status_update(self, event):
        # event chứa data mà Celery gửi sang
        message = event['message']
        data = event['data']

        # Gửi JSON về cho Frontend
        await self.send(text_data=json.dumps({
            'type': 'ORDER_UPDATE',
            'message': message,
            'data': data
        }))