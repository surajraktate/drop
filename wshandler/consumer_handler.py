from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from mydataonline.constants import WEB_SOCKET_CATEGORY_LIST, WEB_SOCKET_CATEGORY_DICT
from mydataonline.utils import get_encrypted_decrypted_name
from clipboard.consumer_handler import get_clipboard_data, store_message_into_database
from file.consumer_handler import get_file_data


class WSHandler(WebsocketConsumer):

    def connect(self):
        """In this function we only create room"""
        self.room_name = None
        self.room_ip = None
        if len(self.scope['url_route']['kwargs']) > 0:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
        if not self.room_name:
            self.room_ip = self.scope.get("client")[0]
        name_for_room = self.room_ip and self.room_ip or self.room_name
        self.room_group_name = 'ws_%s' % name_for_room
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        initial_data = self.get_initial_data()

        self.send(text_data=json.dumps({
            'category': WEB_SOCKET_CATEGORY_DICT.get('ALL_DATA'),
            'data': initial_data,
            'session_id': get_encrypted_decrypted_name(name_for_room, 0)
        }))

    def disconnect(self, close_code):
        # Leave room group
        print("close_code ", close_code)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        request_message_dict = json.loads(text_data)
        message = request_message_dict.get('data')
        category = request_message_dict.get('category')
        if category not in WEB_SOCKET_CATEGORY_LIST:
            self.send(text_data=json.dumps({
                'category': "ERROR",
                'error': "Category not present in list"
            }))
            return
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': category,
                'message': message
            }
        )

    def MESSAGE(self, event):
        print("MESSAGE", event)

    def FILE(self, event):
        print("FILE", event)
        file_data = get_file_data(self.room_name, self.room_ip)
        self.send(text_data=json.dumps({
            'category': WEB_SOCKET_CATEGORY_DICT.get('FILE'),
            'data': json.dumps({"file_data": file_data})
        }))

    def CLIPBOARD(self, event):
        clipboard_data = {
            "room_name": self.room_name,
            "room_ip": self.room_ip,
            "room_data": event.get("message")
        }
        store_message_into_database(clipboard_data)
        self.send(text_data=json.dumps({
            'category': WEB_SOCKET_CATEGORY_DICT.get('CLIPBOARD'),
            'data': event.get("message")
        }))
        
    def get_initial_data(self):
        clipboard_data = get_clipboard_data(self.room_name, self.room_ip)
        file_data = get_file_data(self.room_name, self.room_ip)
        return json.dumps({"clipboard_data": clipboard_data, "file_data": file_data})

