import openai

# Установите ваш API ключ
openai.api_key = 'ваш_api_ключ_здесь'

# Пример запроса к модели
response = openai.Completion.create(
  engine="text-davinci-003",  # или другая модель
  prompt="Привет, как дела?",
  max_tokens=50
)

# Вывод ответа
print(response.choices[0].text.strip())