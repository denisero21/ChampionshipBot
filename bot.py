import logging
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types


TOKEN = os.getenv('BOT_TOKEN')
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
players = types.KeyboardButton('Игроки')
cards = types.KeyboardButton('Карточки')
games = types.KeyboardButton('Игры')
stickers = types.KeyboardButton('Стикеры')
markup.add(players, cards, games, stickers)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Привет, дружочек, ты находишься в главном меню.', reply_markup=markup)

@dp.message_handler(lambda message: message.text == 'Игроки')
async def players_func(message: types.Message):
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
    await message.reply('Выбирай своего кумира и смотри его статистику.', reply_markup=inline_markup)

@dp.message_handler(lambda message: message.text == 'Карточки')
async def cards_func(message: types.Message):
    await message.reply('Скоро..', reply_markup=markup)

@dp.message_handler(lambda message: message.text == 'Игры')
async def games_func(message: types.Message):
    await message.reply('Игры пока в режиме разработки, жди обновлений, братишка.', reply_markup=markup)

@dp.message_handler(lambda message: message.text == 'Стикеры')
async def stickers_func(message: types.Message):
    await message.reply('Стикеры пока в режиме разработки, жди обновлений, братишка.', reply_markup=markup)


#callbacks

@dp.callback_query_handler(text='main')
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer('Ты вернулся в главное меню.', reply_markup=markup)


logging.basicConfig(level=logging.INFO)
start_webhook(
    dispatcher=dp,
    webhook_path=WEBHOOK_PATH,
    skip_updates=True,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    host=WEBAPP_HOST,
    port=WEBAPP_PORT,
)