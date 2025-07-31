# KunAshykBot

Telegram-бот, который умеет:
- Показывать текущую погоду в любом городе мира (через OpenWeatherMap)
- Играть с пользователем в "Камень, ножницы, бумага"
- Работать с обычными и инлайн-кнопками

---

## Стек технологий

- Python 3.10+
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- requests
- python-dotenv
- OpenWeatherMap API
- Railway — деплой

---

## Установка

1. Клонируй репозиторий:

```bash
git clone https://github.com/ZharasAT/weather-chat-bot.git
cd weather-chat-bot
```

2. Создай и активируй виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv/Scripts/activate     # для Windows
```

3. Установи зависимости:

`pip install -r requirements.txt`

4. Создай .env файл и добавь ключи:

```bash
BOT_TOKEN=your_telegram_bot_token
WEATHER_API_KEY=your_openweathermap_api_key
```

5. Запусти бота:

`python main.py`

## Как работает бот

`/start` — показывает меню с выбором

`"Прогноз погоды"` — бот запрашивает название города (на английском!) и возвращает текущую температуру, влажность, ветер

`"Поиграть в игру"` — бот предлагает сыграть в "Камень, ножницы, бумага"

## Деплой на Railway

1. Подключи GitHub-репозиторий

2. Укажи команду запуска:

`python main.py`

3. В разделе Variables добавь:

```bash
BOT_TOKEN=...
WEATHER_API_KEY=...
```

Автор
Разработано [https://github.com/ZharasAT](https://github.com/ZharasAT)