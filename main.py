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
