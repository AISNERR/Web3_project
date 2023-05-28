import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
 

# Replace YOUR_TOKEN with your Telegram bot token
bot = telebot.TeleBot('6238604932:AAHN-8WET49fAFgtEQsBDhYEJR6V7gNAw7E')

# Start command
@bot.message_handler(commands=['start'])
def start_command(message):
    # Creating a menu with buttons
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add(KeyboardButton('Юридические вопросы'), KeyboardButton('Налоги'), KeyboardButton('Поиск компаний'),
             KeyboardButton('Аналитика рынка'))

    # Sending the menu to the user
    bot.send_message(message.chat.id, 'Добро пожаловать в Бизнес Ассистент tada.team. Выбирите пожалуйста опцию бизнес вопросов.', reply_markup=menu)

# Stop command
@bot.message_handler(commands=['stop'])
def stop_command(message):
    # Removing the menu
    remove_menu = ReplyKeyboardRemove()

    # Sending a message to confirm the menu has been removed
    bot.send_message(message.chat.id, 'Меню удалено.', reply_markup=remove_menu)


# Start button
@bot.message_handler(func=lambda message: message.text == 'Start')
def start_button(message):
    # Creating an inline keyboard with the start button
    start_button = InlineKeyboardMarkup()
    start_button.add(InlineKeyboardButton('Start', callback_data='start'))

    # Sending the inline keyboard to the user
    bot.send_message(message.chat.id, 'Нажмите кнопку, чтобы начать:', reply_markup=start_button)

# Stop button
@bot.message_handler(func=lambda message: message.text == 'Stop')
def stop_button(message):
    # Creating an inline keyboard with the stop button
    stop_button = InlineKeyboardMarkup()
    stop_button.add(InlineKeyboardButton('Stop', callback_data='stop'))

    # Sending the inline keyboard to the user
    bot.send_message(message.chat.id, 'Нажмите кнопку, чтобы остановить:', reply_markup=stop_button)

# Callback query handler for the inline buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'start':
        # Do something when the start button is pressed
        bot.answer_callback_query(call.id, text='Starting...')
    elif call.data == 'stop':
        # Do something when the stop button is pressed
        bot.answer_callback_query(call.id, text='Stopping...')

# Start button for specific topics
@bot.message_handler(func=lambda message: message.text == 'Налоги')
def legal_button(message):
    bot.send_message(message.chat.id, f'Я могу помочь определить попало ли юридическое лицо в нетивные реестры ФНС. \
Введите пожалуйста номер ИНН или ОГРН юридического лица в формате "12345678-номер"')
    
@bot.message_handler(func=lambda message: message.text.endswith("номер"))
def answer_legal_button(message):
    message_with_number = '-'.join(message.text.split('-')[:-1])

    def  get_data():
        url = 'https://api-fns.ru/api/check'
        params = { 'key': '231f6fc2b1d5545a73d0eeba4655c68653854903',
                'format': 'json',
                'req': f'{str(message_with_number)}',
                
                } 
        r = requests.get(url,  params=params)
        result = r.json()
        return result
    response = get_data()

    answer_dict = {
                    "ОГРН":  None,
                    "ИНН":  None,
                    "Позитив": None,
                    "Негатив":  None,
                }
    
    for option in response["items"]:
        for sortion in option:
            answer_dict["ОГРН"] = option[sortion].get("ОГРН")
            answer_dict["ИНН"] = option[sortion].get("ИНН")
            answer_dict["Позитив"] = option[sortion].get("Позитив")
            answer_dict["Негатив"] = option[sortion].get("Негатив")

    if answer_dict.get("Негатив") is None:
        response_from_bot = f"Данное юридическое лицо не попало в негативные реестры ФНС, отметки \
    о недостоверных данных, признаки «массового» директора, учредителя, решений о ликвидации, \
    реорганизации и прочие"
    else:
        response_from_bot = f'Данное юридическое лицо попало в негативные реестры ФНС, найдены отметки \
    о недостоверных данных, признаки «массового» директора, учредителя, решений о ликвидации, \
    реорганизации и прочие. Инн: {answer_dict["ИНН"]}. ОГРН {answer_dict["ОГРН"]}. Дополнительная информация: \
    Статус:{answer_dict["Негатив"]["Статус"]}, Недостоверный адрес: {answer_dict["Негатив"]["НедостоверАдрес"]}, \
    МассРук: {answer_dict["Негатив"]["МассРук"]}, РукЛиквКомп: {answer_dict["Негатив"]["РукЛиквКомп"]}, \
    НедостоверРук: {answer_dict["Негатив"]["НедостоверРук"]}, Дополнительно: {answer_dict["Негатив"]["Текст"]}'
    bot.send_message(message.chat.id, response_from_bot)
    bot.send_message(message.chat.id, "Пожалуйста ответьте, на сколько по шкале от 1 до 5 \
    вы довольны моей работой в формате '1-оценка' ")


@bot.message_handler(func=lambda message: message.text == 'Юридические вопросы')
def tax_button(message):
    # Do something when the tax button is pressed
    bot.send_message(message.chat.id, 'Вы выбрали Юридические вопросы.')

@bot.message_handler(func=lambda message: message.text == 'Поиск компаний')
def company_search_button(message):
    # Do something when the company search button is pressed
    bot.send_message(message.chat.id, 'Вы выбрали поиск компаний.')

@bot.message_handler(func=lambda message: message.text == 'Аналитика рынка')
def market_analytics_button(message):
    # Do something when the market analytics button is pressed
    bot.send_message(message.chat.id, 'Вы выбрали аналитику рынка.')

# Stop command
@bot.message_handler(commands=['stop'])
def stop_command(message):
    # Removing the menu
    remove_menu = ReplyKeyboardRemove()

    # Sending a message to confirm the menu has been removed
    bot.send_message(message.chat.id, 'Menu removed.', reply_markup=remove_menu)


# Start button
@bot.message_handler(func=lambda message: message.text == 'Start')
def start_button(message):
    # Creating an inline keyboard with the start button
    start_button = InlineKeyboardMarkup()
    start_button.add(InlineKeyboardButton('Start', callback_data='start'))

    # Sending the inline keyboard to the user
    bot.send_message(message.chat.id, 'Press the button to start:', reply_markup=start_button)

# Stop button
@bot.message_handler(func=lambda message: message.text == 'Stop')
def stop_button(message):
    # Creating an inline keyboard with the stop button
    stop_button = InlineKeyboardMarkup()
    stop_button.add(InlineKeyboardButton('Stop', callback_data='stop'))

    # Sending the inline keyboard to the user
    bot.send_message(message.chat.id, 'Press the button to stop:', reply_markup=stop_button)

@bot.message_handler(func=lambda message: message.text.endswith("оценка"))
def answer_legal_button(message):
    message_with_number = '-'.join(message.text.split('-')[:-1])
    if message_with_number == '1':
        bot.send_message(message.chat.id,  "разработчики учтут ваше мнение \
и обязательно улучшат бота")
    if message_with_number == '3':
        bot.send_message(message.chat.id, "спасибо за среднюю оценку, \
мы обязательно будем улучшаться !" )
    if message_with_number == '5':
        bot.send_message(message.chat.id,  "спасибо за высокую оценку !")


# Callback query handler for the inline buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'start':
        # Do something when the start button is pressed
        bot.answer_callback_query(call.id, text='Starting...')
    elif call.data == 'stop':
        # Do something when the stop button is pressed
        bot.answer_callback_query(call.id, text='Stopping...')

# Start the bot
bot.polling()