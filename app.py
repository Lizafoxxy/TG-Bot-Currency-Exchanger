import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

#обработчик команд start и help
@bot.message_handler(commands = ['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: <название валюты, которую меняем> <в какую валюту перевести> <размер суммы для пересчета>\n Чтобы увидеть список всех доступных для конвертации валют: /values'
    bot.reply_to(message, text)

#обработчик команды values
@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Валюты доступные для конвертации:\n '
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

# обработчик запроса от пользователя, который он будет вводить: там будет валюта, во что переводить и количетсво
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException ('Неправильное количество параметров.')

        base, quote, amount = values
        total_base = round(CurrencyConverter.get_price(base, quote, amount)*float(amount), 2)

    #если ошибка допущена пользователем при вводе данных
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    #если ошибка произошла не по вине пользователя, а на стороне сервера
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    #если все в порядке, то запрос пользователя обрабатывается
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()


