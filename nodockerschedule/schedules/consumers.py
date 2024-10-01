import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ScheduleConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None
        self.schedule_id = None

    async def connect(self):
        self.schedule_id = self.scope['url_route']['kwargs']['schedule_id']
        self.group_name = f'schedule_{self.schedule_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def new_event(self, event):
        await self.send(text_data=json.dumps(event['event']))
