import telebot
from pass_key import TOKEN, exchanges
from extensions import Conversion, ConvertionException
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = "Чтобы я вам помог конвертировать валюту, введите комнаду в следующем формате:\n<имя валюты> (пробел) \
<в какую валюту переводить> (пробел) \
<какое кол-во валюты вы хотите перевести>\nУвидеть список доступных валют можно при помощи команды: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for i in exchanges.keys():
        text = "\n".join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionException("Вы ввели неправильное кол-во параметров")

        quote, base, amount = values
        answer = Conversion.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Зафиксирована следущая ошибка пользователя:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"не удалось обработать команду\n{e}")
    else:
        text = f"При конвертации {amount} {quote} вы получаете {answer} {base}"
        bot.send_message(message.chat.id, text)



bot.polling()