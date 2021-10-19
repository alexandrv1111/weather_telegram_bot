import telebot
from pyowm import OWM
import json


t = '2072732993:AAF7WeOhb2n337Sle5658HZDXSKGQJA_Ly8'
owm = OWM('1cf170c90f40b0c407f740d74f58e54c')

bot = telebot.TeleBot(t, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    mgr = owm.weather_manager()
    observation = None
    try:
        observation = mgr.weather_at_place(message.text)
    except Exception:
        bot.send_message(message.chat.id, 'No city')  # message.text)

    w = observation.weather

    result = {
        'City': message.text,
        'wind speed': w.wind()['speed'],
        'wind direction': w.wind()['deg'],
        'humidity': w.humidity,
        'temperature now': w.temperature('celsius')['temp'],
        'min temperature': w.temperature('celsius')['temp_min'],
        'max temperature': w.temperature('celsius')['temp_max'],
        'rain': w.rain,
        'clouds': w.clouds
    }

    ans = ''
    ans3 = json.dumps(result)
    for k,v in result.items():
        ans += str(k)+(': ') + str(v) + '\n'  #message.text)
    print(ans)
    print(w)

    bot.send_message(message.chat.id, ans)  #message.text)

bot.infinity_polling()