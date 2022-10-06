import requests
import telebot
import json

bot = telebot.TeleBot(json.load(open("./secrets.json"))[0])
first_cord = 0
second_cord = 0


def get_wheater_data(url):
    data = json.loads(requests.get(url).text)
    context = {
        "температура": [data['main']['temp'], "°C"],
        "влажность": [data['main']['humidity'], "%"],
        "скорость ветра": [data['wind']['speed'], "км/ч"],
        "облачность": [data['clouds']['all'], "%"],
    }
    return context


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text.lower() == "поехали":
        bot.send_message(message.from_user.id, 'Введите первую координату')
        bot.register_next_step_handler(message, get_first_cord)
    else:
        bot.send_message(message.from_user.id, 'Напишите поехали')

def get_first_cord(message):
    global first_cord
    try:
        first_cord = float(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, 'Введите пожалуйста число')
        bot.register_next_step_handler(message, get_first_cord)
    else:
        bot.send_message(message.from_user.id, 'Введите вторую координату')
        bot.register_next_step_handler(message, get_second_cord)


def get_second_cord(message):
    global second_cord
    try:
        second_cord = float(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, 'Введите пожалуйста число')
        bot.register_next_step_handler(message, get_second_cord)
    else:
        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid=" + json.load(open("./secrets.json"))[1]
        data = get_wheater_data(url.format(first_cord, second_cord))
        for key, value in data.items():
            bot.send_message(message.from_user.id, f"{key}: {value[0]}{value[1]}")

bot.polling(none_stop=True, interval=0)
