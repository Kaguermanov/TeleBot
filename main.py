import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "Добро пожаловать! Чтобы узнать цену валюты, отправьте сообщение в формате:\n"
        "<имя валюты> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\n"
        "Пример: евро доллар 100\n"
        "Доступные команды:\n"
        "/values - список доступных валют"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = "Доступные валюты:\nевро, доллар, рубль"
    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
def convert(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException("Неверное количество параметров. Должно быть три параметра.")

        base, quote, amount = values
        result = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e}")
    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка: {e}")
    else:
        text = f"Цена {amount} {base} в {quote} = {result}"
        bot.reply_to(message, text)


bot.polling()


