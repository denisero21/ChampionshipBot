import telebot;
from telebot import types
from datetime import datetime
token = '5729426425:AAEN1FvNh6cLhS92fAcSfDxH5LgCyHbQ998'
bot_username='denisero_bot'
bot = telebot.TeleBot(f'{token}')


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
players = types.KeyboardButton('Игроки')
cards = types.KeyboardButton('Карточки')
games = types.KeyboardButton('Игры')
stickers = types.KeyboardButton('Стикеры')
markup.add(players, cards, games, stickers)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        text=f"Привет, дружочек, ты находишься в главном меню.",
        reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == 'Игроки'):
        inline_markup = types.InlineKeyboardMarkup(row_width=1)
        koz = types.InlineKeyboardButton(text='Владислав Козлов', callback_data='koz')
        kava = types.InlineKeyboardButton(text='Артем Ковальчук', callback_data='kava')
        den = types.InlineKeyboardButton(text='Денис Ерощенко', callback_data='den')
        victor = types.InlineKeyboardButton(text='Виктор Мармулев', callback_data='victor')
        orange = types.InlineKeyboardButton(text='Даниил Курленко', callback_data='orange')
        sham = types.InlineKeyboardButton(text='Илья Шемяков', callback_data='sham')
        dmitriy = types.InlineKeyboardButton(text='Дмитрий Авдейчук', callback_data='dmitriy')
        flesh = types.InlineKeyboardButton(text='Илья Сугако', callback_data='flesh')
        litosh = types.InlineKeyboardButton(text='Алексей Литош', callback_data='litosh')
        ferb = types.InlineKeyboardButton(text='Никита Запотылок', callback_data='ferb')
        iceman = types.InlineKeyboardButton(text='Андрей Мороз', callback_data='iceman')
        fadeev = types.InlineKeyboardButton(text='Павел Фадеев', callback_data='fadeev')
        legend = types.InlineKeyboardButton(text='Руслан Колесников', callback_data='legend')
        luba = types.InlineKeyboardButton(text='Илья Любченко', callback_data='luba')
        bread = types.InlineKeyboardButton(text='Кирилл Твердохлеб', callback_data='bread')
        danilov = types.InlineKeyboardButton(text='Даниил Данилов', callback_data='danilov')
        kreed = types.InlineKeyboardButton(text='Егор Данилов', callback_data='kreed')
        schegrin = types.InlineKeyboardButton(text='Иван Щегринов', callback_data='schegrin')
        solovyan = types.InlineKeyboardButton(text='Глеб Соловянчик', callback_data='solovyan')
        maks = types.InlineKeyboardButton(text='Максим Яковлев', callback_data='maks')
        busel = types.InlineKeyboardButton(text='Илья Бусел', callback_data='busel')
        nikolas = types.InlineKeyboardButton(text='Николай Клочко', callback_data='nikolas')
        shenets = types.InlineKeyboardButton(text='Роман Шенец', callback_data='shenets')


        main = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main')
        inline_markup.add(koz, kava, den, sham, victor, orange, dmitriy, flesh, litosh, ferb, iceman, fadeev,
            legend, luba, bread, danilov, kreed, schegrin, solovyan, maks, busel, nikolas, shenets, main)
        bot.send_message(message.chat.id, 
            text='Выбирай своего кумира и смотри его статистику.',
            reply_markup=inline_markup)
    elif(message.text == 'Карточки'):
        pass
    elif(message.text == 'Игры'):
        bot.send_message(message.chat.id, 
            text='Игры пока в режиме разработки, жди обновлений, братишка.', 
            reply_markup=markup)
    elif message.text == 'Стикеры':
        bot.send_message(message.chat.id, 
            text='Стикеры пока в режиме разработки, жди обновлений, братишка.', 
            reply_markup=markup)
    elif message.text == 'Вернуться в главное меню':
        bot.send_message(message.chat.id, text='Ты вернулся в главное меню.', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'main':
        bot.send_message(call.message.chat.id, text='Ты вернулся в главное меню.', reply_markup=markup)
    elif call.data == 'top_up':
        pass
    elif call.data == 'withdraw':
        pass

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)