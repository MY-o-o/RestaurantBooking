import json

from channels.generic.websocket import AsyncWebsocketConsumer


class TableStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('tables', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('tables', self.channel_name)

    async def table_status(self, event):
        await self.send(text_data=json.dumps({
            'table_id': event['table_id'],
            'status': event['status'],
            'date': event.get('date'),
            'time': event.get('time'),
        }))
