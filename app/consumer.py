import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.receiver_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = f'chat_{min(self.user.id,int(self.receiver_id))}_{max(self.user.id,int(self.receiver_id))}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Enregistrer le message dans la DB
        await sync_to_async(Message.objects.create)(sender=self.user,
                                                    receiver_id=self.receiver_id,
                                                    message=message)

        # Envoyer à tout le groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.user.id,
                'timestamp': str(int(Message.objects.last().date.timestamp()))
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
