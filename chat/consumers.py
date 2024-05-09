import base64
import json
import jwt
import secrets
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Message, Conversation
from .serializers import MessageSerializer

UserProfile = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        headers_dict = dict((key.decode(), value.decode()) for key, value in self.scope['headers'])
        token = headers_dict.get('authorization')
        if not token:
            self.close()
            return
        
        if not self.validate_token(token):
            self.close()
            return
        
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload['user_id']

    def disconnect(self, close_code):
        # pass
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        try:
            text_data_json = json.loads(text_data)
            chat_type = {"type": "chat_message"}
            return_dict = {**chat_type, **text_data_json}
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                return_dict,
            )
        except Exception as e:
            print(f"Error processing message: {e}")
            self.close()

    def chat_message(self, event):
        try:
            text_data_json = event.copy()
            text_data_json.pop("type")
            message = text_data_json.get("message")
            attachment = text_data_json.get("attachment")
            conversation = Conversation.objects.get(id=int(self.room_name))
            sender  = UserProfile.objects.get(id=self.user_id)
            if not isinstance(sender, UserProfile):
                sender = UserProfile.objects.get(id=sender.id)
            if attachment:
                file_str, file_ext = attachment.get("data"), attachment.get("format")
                
                file_data = ContentFile(
                    base64.b64decode(file_str),
                    name=f"{secrets.token_hex(8)}.{file_ext}"
                )
                message_obj = Message.objects.create(
                    sender=sender,
                    attachment=file_data,
                    text=message,
                    conversation=conversation,
                )
            else:
                message_obj = Message.objects.create(
                    sender=sender,
                    text=message,
                    conversation=conversation,
                )
            serializer = MessageSerializer(instance=message_obj)
            self.send(text_data=json.dumps(serializer.data))
            
        except UserProfile.DoesNotExist:
            print("UserProfile matching query does not exist.")
        except Exception as e:
            print(f"Error in chat_message: {e}")
            self.close()
    

    def validate_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            print("Token has expired")
        except jwt.InvalidTokenError:
            print("Invalid token")

        return False
