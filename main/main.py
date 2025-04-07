import requests
import logging
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseSettings

# Явно объявляем экспортируемые символы
__all__ = ['Settings', 'DeepSeekClient', 'main']

# Загрузка переменных окружения
load_dotenv()

class Settings(BaseSettings):
    api_key: str

    class Config:
        env_file = ".env"

try:
    settings = Settings()
except Exception as config_error:
    raise ValueError(f"Ошибка конфигурации: {config_error}")

logging.basicConfig(level=logging.INFO)

class DeepSeekClient:
    def __init__(self):
        self.api_key = settings.api_key
        self.api_url = "https://api.deepseek.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()

    def send_message(self, message: str, model: str = "deepseek-chat-v1", max_tokens: int = 50) -> Optional[str]:
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": message}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        try:
            response = self.session.post(
                self.api_url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.Timeout:
            logging.error("Таймаут запроса")
            return None
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP ошибка: {http_err.response.status_code}")
            return None
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Ошибка запроса: {req_err}")
            return None

def main():
    client = DeepSeekClient()
    response = client.send_message("Привет, как дела?")
    if response:
        logging.info(f"Ответ DeepSeek: {response}")
    else:
        logging.error("Не удалось получить ответ от DeepSeek API")

if __name__ == "__main__":
    main()