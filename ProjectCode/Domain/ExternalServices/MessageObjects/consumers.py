from channels.generic.websocket import AsyncWebsocketConsumer

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f'user_{user_id}'

        # Add the user to the channel group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the channel group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Handle incoming WebSocket messages, if needed
        pass

    async def message(self, event):
        # Send the message to the WebSocket connection
        await self.send(text_data=event['message'])
