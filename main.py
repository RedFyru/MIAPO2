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


@bot.callback_query_handler(func=lambda call: True)
def number_of_lucky_tickets(call):
    if call.data == 'res':
        ticket_range = range_of_tickets.get(call.message.chat.id)
        if ticket_range:
            start_number, end_number = ticket_range
            result = count_lucky_tickets(start_number, end_number)
            message_text = f'📌Количество счастливых билетов: {result}\n'
            shortest_gap, longest_gap = find_shortest_longest_gaps(start_number, end_number)
            even_count, odd_count, prime_count, palindrome_count, divisible_count = (count_even_odd_prime_palindrome_divisible_tickets
                                                                                     (start_number, end_number))
            square_count, cube_count = count_squares_cubes(start_number, end_number)
            if shortest_gap:
                message_text += (f'📌Самый короткий промежуток между счастливыми билетами: '
                                 f'{shortest_gap[0]} - {shortest_gap[1]}\n')
            else:
                message_text += '📌Нет коротких промежутков между счастливыми билетами.\n'
            if longest_gap:
                message_text += (f'📌Самый длинный промежуток между счастливыми билетами: '
                                 f'{longest_gap[0]} - {longest_gap[1]}\n')
            else:
                message_text += '📌Нет длинных промежутков между счастливыми билетами.\n'
            message_text += f'📌Количество четных счастливых билетов: {even_count}\n'
            message_text += f'📌Количество нечетных счастливых билетов: {odd_count}\n'
            message_text += f'📌Количество протсых счастливых билетов: {prime_count}\n'
            message_text += f'📌Количество счастливых билетов, являющихся полными квадратами: {square_count}\n'
            message_text += f'📌Количество счастливых билетов, являющихся полными кубами: {cube_count}\n'
            message_text += f'📌Количество счастливых билетов, являющихся палиндромами: {palindrome_count}\n'
            message_text += f'📌Количество счастливых билетов, у которых одна половина делится нацело на другую: ' \
                f'{divisible_count}'
            bot.send_message(call.message.chat.id, message_text)
        else:
            bot.send_message(call.message.chat.id, 'Сначала задайте диапазон.')


def count_lucky_tickets(start_range, end_range):
    count = 0
    for ticket_number in range(start_range, end_range + 1):
        if lucky_tickets(ticket_number):
            count += 1
    return count


def lucky_tickets(ticket_number):
    digits = [int(digit) for digit in str(ticket_number).rjust(6, '0')]
    return sum(digits[:3]) == sum(digits[3:])


def find_shortest_longest_gaps(start_long_short, end):
    gaps = []
    current_gap_start = None
    for i in range(start_long_short, end + 1):
        if lucky_tickets(i):
            if current_gap_start is not None:
                gaps.append((current_gap_start, i))
                current_gap_start = None
        elif current_gap_start is None:
            current_gap_start = i
    shortest_gap = min(gaps, key=lambda gap: gap[1] - gap[0]) if gaps else None
    longest_gap = max(gaps, key=lambda gap: gap[1] - gap[0]) if gaps else None
    return shortest_gap, longest_gap


def count_even_odd_prime_palindrome_divisible_tickets(big_start, end):
    prime_count = 0
    even_count = 0
    odd_count = 0
    palindrome_count = 0
    divisible_count = 0
    for i in range(big_start, end + 1):
        if lucky_tickets(i):
            if is_prime(i):
                prime_count += 1
            if i % 2 == 0:
                even_count += 1
            if i % 2 != 0:
                odd_count += 1
            if str(i) == str(i)[::-1]:
                palindrome_count += 1
            if is_divisible(i):
                divisible_count += 1
    return even_count, odd_count, prime_count, palindrome_count, divisible_count


def is_divisible(number):
    num_str = str(number).zfill(6)
    first_part = int(str(num_str)[:3])
    second_part = int(str(num_str)[3:])
    return first_part % second_part == 0 or second_part % first_part == 0


def count_squares_cubes(start_square_cube, end):
    square_count = 0
    cube_count = 0
    for i in range(start_square_cube, end + 1):
        if lucky_tickets(i):
            square_root = int(i ** 0.5)
            cube_root = int(i ** (1 / 3))
            if square_root ** 2 == i:
                square_count += 1
            if cube_root ** 3 == i:
                cube_count += 1
    return square_count, cube_count


def find_square_lucky_tickets(start_square, end):
    square_lucky_tickets = []
    for num in range(start_square, end + 1):
        if lucky_tickets(num):
            square_root = int(num ** 0.5)
            if square_root ** 2 == num:
                square_lucky_tickets.append(num)
    return square_lucky_tickets


def find_lucky_cube_tickets(start_cube, end):
    lucky_cube_tickets = []
    for i in range(start_cube, end + 1):
        if lucky_tickets(i):
            cube_root = int(i ** (1 / 3))
            if cube_root ** 3 == i:
                lucky_cube_tickets.append(i)
    return lucky_cube_tickets


def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True


def density_on_the_graph(start_range, end_range):
    nums = [num for num in range(start_range, end_range + 1) if lucky_tickets(num)]
    fig = px.histogram(x=nums, nbins=50, labels={'x': 'Числа', 'y': 'Количество'},
                       title='Плотность распределения чисел')
    fig.update_layout(yaxis_title_text='Количество')
    fig.update_layout(xaxis_title_text='Числа')
    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)
    return buf


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
