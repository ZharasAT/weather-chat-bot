import os
import random
import requests
import telebot

from dotenv import load_dotenv
from telebot import types

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
bot = telebot.TeleBot(BOT_TOKEN)

user_states = {}


@bot.message_handler(commands=['start'])
def start(message):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("Прогноз погоды")
    btn3 = types.KeyboardButton('Поиграть в "Камень, ножницы, бумага!"')
    reply_markup.add(btn1, btn2, btn3)

    inline_markup = types.InlineKeyboardMarkup(row_width=1)
    inline_markup.add(
        types.InlineKeyboardButton("👋 Поздороваться", callback_data="greet"),
        types.InlineKeyboardButton("Прогноз погоды", callback_data="weather"),
        types.InlineKeyboardButton("Поиграть в игру", callback_data="play")
    )

    bot.send_message(
        message.chat.id,
        "Привет! Я твой бот-синоптик. Пожалуйста, выбери действие:",
        reply_markup=reply_markup
    )

    bot.send_message(
        message.chat.id,
        "(Если ты не видишь кнопки - нажми одну из этих 👇)",
        reply_markup=inline_markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "greet":
        bot.send_message(call.message.chat.id, "Привет, рад тебя видеть!")

    elif call.data == "weather":
        bot.send_message(
            call.message.chat.id,
            (
                "Напиши мне название города **на английском языке** "
                "(например: *Almaty*, *Paris*, *Tokyo*), "
                "и я покажу текущую погоду.",
            ),
            parse_mode="Markdown"
        )
        user_states[call.message.chat.id] = "awaiting_city"

    elif call.data == "play":
        game_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        game_markup.add("Камень", "Ножницы", "Бумага")
        bot.send_message(
            call.message.chat.id,
            "Выбери: камень, ножницы или бумага.",
            reply_markup=game_markup
        )


@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    user_choice = message.text.lower()

    if user_states.get(message.chat.id) == "awaiting_city":
        city_name = message.text.strip()
        weather_info = get_weather(city_name)
        bot.send_message(message.chat.id, weather_info)
        user_states[message.chat.id] = None
        return

    elif message.text == "👋 Поздороваться":
        bot.send_message(message.chat.id, "Привет, рад тебя видеть!")

    elif message.text == "Прогноз погоды":
        bot.send_message(
            message.chat.id,
            "Напиши мне название города, и я скажу, какая там погода."
        )
        user_states[message.chat.id] = "awaiting_city"

    elif message.text == 'Поиграть в "Камень, ножницы, бумага!"':
        game_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        game_markup.add("Камень", "Ножницы", "Бумага")
        bot.send_message(message.chat.id,
                         "Выбери: камень, ножницы или бумага.",
                         reply_markup=game_markup)

    elif user_choice in ["камень", "ножницы", "бумага"]:
        bot_choice = random.choice(["камень", "ножницы", "бумага"])
        result = determine_winner(user_choice, bot_choice)
        bot.send_message(message.chat.id,
                         f"Ты выбрал: {user_choice.capitalize()}\n"
                         f"Бот выбрал: {bot_choice.capitalize()}\n\n"
                         f"{result}")

    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, выбери вариант из меню.")


def determine_winner(user, bot):
    if user == bot:
        return "Ничья! 🤝"
    elif (user == "камень" and bot == "ножницы") or \
         (user == "ножницы" and bot == "бумага") or \
         (user == "бумага" and bot == "камень"):
        return "Ты победил! 🎉"
    else:
        return "Ты проиграл... 😢"


def get_weather(city_name):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name}"
        f"&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    )
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        city = data["name"]
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        return (
            f"📍 Город: {city}\n"
            f"🌤 Погода: {weather.capitalize()}\n"
            f"🌡 Температура: {temp}°C\n"
            f"💧 Влажность: {humidity}%\n"
            f"🌬 Ветер: {wind} м/с"
        )
    elif response.status_code == 404:
        return "⚠️ Город не найден. Попробуй ввести название ещё раз."
    else:
        return "❌ Ошибка при получении погоды."


bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    bot.polling(non_stop=True, interval=0)
