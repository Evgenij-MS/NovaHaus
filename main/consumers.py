from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()  # Установить соединение

    async def disconnect(self, close_code):
        pass  # Обработка разрыва соединения, если требуется

    async def receive(self, text_data=None, bytes_data=None):
        # Убедитесь, что text_data может быть None, поэтому обрабатывайте корректно
        if text_data:
            data = json.loads(text_data)  # Преобразование текста в JSON
            user_input = data.get('message')

            # Ваш обработчик данных
            ai_response = f"Ответ AI на: {user_input}"
            await self.send(json.dumps({'response': ai_response}))
