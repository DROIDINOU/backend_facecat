from channels.generic.websocket import AsyncWebsocketConsumer
import json

def get_room_name(user1, user2):
    # Always order users to ensure the room name is consistent
    if user1 < user2:
        return f'{user1}_{user2}'
    return f'{user2}_{user1}'

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the room name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print("voici room name:", self.room_group_name)
        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message = text_data

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))