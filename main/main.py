import requests
import logging
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseSettings, ValidationError

# Загрузка переменных окружения
load_dotenv()

class Settings(BaseSettings):
    api_key: str

    class Config:
        env_file = ".env"

try:
    settings = Settings()
except ValidationError as e:
    raise ValueError(f"Configuration error: {e}")

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
            response = self.session.post(self.api_url, headers=self.headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.Timeout:
            logging.error("Request timed out")
            return None
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code}")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            return None

def main():
    client = DeepSeekClient()
    response = client.send_message("Hello, how are you?")
    if response:
        logging.info(f"DeepSeek response: {response}")
    else:
        logging.error("Failed to get a response from DeepSeek API")

if __name__ == "__main__":
    main()
