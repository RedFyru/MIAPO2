import telebot
from telebot import types
import io
import plotly.express as px

bot = telebot.TeleBot('6979821341:AAEw_fzAoPsK52diJw_4pEG5onP3PC1vS6Q')

range_of_tickets = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    range_button = types.KeyboardButton('Задать диапазон')
    build_graph_button = types.KeyboardButton('Построить график')
    markup.add(range_button, build_graph_button)
    bot.send_message(message.chat.id, f'Привет! {message.from_user.first_name}👋\n'
                                      f'Добро пожаловать в мир "Счастье в билетах"!🎉🎫\n'
                                      f'Я готов помочь тебе узнать интересные факты, строить графики распределения, '
                                      f'и даже обнаруживать самые удивительные числа! '
                                      f'Я подготовлю для тебя увлекательные статистические данные 📊💫\n'
                                      f'Что бы продолжить выберите действие:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Задать диапазон')
def set_range(message):
    bot.send_message(message.chat.id, 'Введите 2 числа в диапазоне от 1 до 999999 через пробел.')
    bot.register_next_step_handler(message, users_input)


def users_input(message):
    markup = types.InlineKeyboardMarkup()
    result = types.InlineKeyboardButton('Результаты', callback_data='res')
    markup.add(result)
    try:
        start_number, end_number = map(int, message.text.split())
        if 1 <= start_number <= 999999 and 1 <= end_number <= 999999 and start_number <= end_number:
            formatted_start_number = f'{start_number:06d}'
            formatted_end_number = f'{end_number:06d}'
            range_of_tickets[message.chat.id] = (start_number, end_number)
            bot.reply_to(message, f'Ваш даипазон: {formatted_start_number}:{formatted_end_number}', reply_markup=markup)
        else:
            bot.reply_to(message, 'Пожалйуста введите числа в диапазоне от 1 до 999999.')
    except ValueError:
        bot.reply_to(message, 'Пожалуйста введите корректные числа через пробел.')

