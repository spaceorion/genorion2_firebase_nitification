from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from random import randint
import json
import time
from time import sleep
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from .models import *
from .serializers import *
from rest_framework.response import Response
from channels.db import database_sync_to_async
from django.http import HttpResponse
from rest_framework import status
from django.http import HttpResponse
from django.http import JsonResponse

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        # Join room
        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            # self.room_group_name,
            self.channel_name
        )
    
    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        d_id = data['d_id']
        healthS1 = data['healthS1']
        healthS2 = data['healthS2']
        healthS3 = data['healthS3']
        healthS4 = data['healthS4']

        await self.save_message(d_id, healthS1, healthS2, healthS3, healthS4)

        # Send message to room group
        # await self.channel_layer.group_send(
        #     # self.room_group_name,
        #     {
        #         # 'type': 'chat_message',
        #         # 'd_id' : d_id,
        #         'healthS1' : healthS1,
        #         'healthS2': healthS2,
        #         'healthS3': healthS3,
        #         'healthS4': healthS4
        #     }
        # )
    
    # Receive message from room group
    async def chat_message(self, event):
        
        d_id = event['d_id']
        print("dfsgsgsdfg", d_id)
        healthS1 = event['healthS1']
        healthS2 = event['healthS2']
        healthS3 = event['healthS3']
        healthS4 = event['healthS4']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'd_id' : d_id,
            'healthS1' : healthS1,
            'healthS2' : healthS2,
            'healthS3' : healthS3,
            'healthS4' : healthS4
        }))

    @sync_to_async
    def save_message(self, d_id, healthS1, healthS2, healthS3, healthS4):
        d_id = allDevices(d_id=d_id)
        if healthrecord.objects.filter(d_id=d_id).exists:
            # df = healthrecord.objects.filter(d_id=d_id)
            # dfJson = recordhealthSerializers(df, many=True)
            t = healthrecord.objects.get(d_id=d_id)
            t.healthS1 = healthS1
            t.healthS2 = healthS2
            t.healthS3 = healthS3
            t.healthS4 = healthS4
            t.save()
            print("updated")
        else:
            healthrecord.objects.create(d_id=d_id, healthS1=healthS1, healthS2=healthS2, healthS3=healthS3, healthS4=healthS4)
            print("created...!!!")