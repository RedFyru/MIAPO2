import telebot
from telebot import types
import io
import plotly.express as px

bot = telebot.TeleBot('6979821341:AAEw_fzAoPsK52diJw_4pEG5onP3PC1vS6Q')

range_of_tickets = {}


@bot.message_handler(func=lambda message: message.text == 'Построить график')
def schedule(message):
    ticket_range = range_of_tickets.get(message.chat.id)
    if ticket_range:
        start_number, end_number = ticket_range
        plot_buf = density_on_the_graph(start_number, end_number)
        bot.send_photo(message.chat.id, plot_buf,
                       caption='График расположения cчастливых билетов на числовом промежутке:')
    else:
        bot.send_message(message.chat.id, 'Сначала задайте диапазон.')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, 'Пожалуйста используйте меня по назначению')


bot.polling(none_stop=True, interval=5)