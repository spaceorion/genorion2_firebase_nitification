import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import  allDevices ,deviceStatus

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        d_id = data['d_id']
        sensor1 = data['sensor1']
        sensor2=data['sensor2']
        # username = data['username']
        # room = data['room']

        await self.save_message(d_id, sensor1,sensor2)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                 'd_id':d_id,
                'sensor1': sensor1,
                'sensor2': sensor2,

                
            }
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        d_id=event['d_id']
        sensor1 = event['sensor1']
        sensor2 = event['sensor2']

       

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'd_id':d_id,
            'sensor1': sensor1,
            'sensor2': sensor2,

            
            
        }))
    @sync_to_async
    def save_message(self, d_id, sensor1,sensor2):
        d_id = allDevices(d_id=d_id)
        if deviceStatus.objects.filter(d_id=d_id).exists:
            # df = healthrecord.objects.filter(d_id=d_id)
            # dfJson = recordhealthSerializers(df, many=True)
            t = deviceStatus.objects.get(d_id=d_id)
            
            t.sensor1 =sensor1
            t.sensor2 = sensor2
            t.save()
            print("updated")
        else:
            deviceStatus.objects.create(d_id=d_id, sensor1=sensor1,sensor2=sensor2)
            print("created...!!!")

    # @sync_to_async
    # def save_message(self, username, room, sensor1,sensor2):
    #     Message.objects.create(username=username, room=room,sensor1=sensor1,sensor2=sensor2)