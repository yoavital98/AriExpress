from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from ProjectCode.Domain.ExternalServices.MessageController import send_notification


class MessageObserver:

    def __init__(self, user_id):
        self.user_id = user_id

    def update(self, message):
        channel_layer = get_channel_layer()

        # Send the message to the recipient's channel group
        async_to_sync(channel_layer.group_send)(
            f"user_{message.receiver_id}",
            {
                'type': 'message',
                'message': message.toJson(),
            }
        )

        send_notification(message.receiver_id, "You have a new message")
