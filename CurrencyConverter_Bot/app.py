import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def help(message: telebot.types.Message):
    text = f'Здравствуйте, {message.from_user.first_name}!\nЭто бот-конвертер валют.\nДля того,чтобы узнать, как пользоваться ботом, \
нажмите /help\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты, цену которой Вы хотите узнать> \
<валюта, в которую Вы хотите перевести первую валюту> \
<количество первой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Слишком много/мало параметров.')
        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote}  - {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
