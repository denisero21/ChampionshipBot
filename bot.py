from aiogram import Bot, Dispatcher, executor, types
import config
import asyncpg


USER = config.USER
PASSWORD = config.PASSWORD
DB = config.DB
HOST = config.HOST

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


# markups

main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
seasons = types.KeyboardButton('Сезоны')
players = types.KeyboardButton('Игроки')
cards = types.KeyboardButton('Карточки')
games = types.KeyboardButton('Игры')
stickers = types.KeyboardButton('Стикеры')
main_markup.add(seasons, players, cards, games, stickers)


seasons_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
shpl16 = types.KeyboardButton('ШПЛ16')
shpl17 = types.KeyboardButton('ШПЛ17')
shpl4 = types.KeyboardButton('ШПЛ4')
bhshpl = types.KeyboardButton('БХШПЛ')
bhshpl1 = types.KeyboardButton('БХШПЛ1')
back = types.KeyboardButton('Вернуться в главное меню')
seasons_markup.add(shpl16, shpl17, shpl4, bhshpl, bhshpl1, back)

def set_season(champ_str: str, cup_str: str, top_str:str):
    season_markup = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    champ = types.InlineKeyboardButton('Чемпионат', callback_data=f'{champ_str}')
    cup = types.InlineKeyboardButton('Кубок', callback_data=f'{cup_str}')
    top = types.InlineKeyboardButton('Топ игроков', callback_data=f'{top_str}')
    season_markup.add(champ, cup, top)
    return season_markup

async def get_players():
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    players_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    rows_names = []
    for i in range(1,48):
        rows_names.append(await db_connect.fetchrow('select name from player where id = $1', i))
    rows_names = list(set(rows_names))
    rows_players = [] 
    for i in rows_names:
        rows_players.append(await db_connect.fetchrow('SELECT player.name, COUNT(goal.player_id) as goals'+
            ' FROM player'+
            ' LEFT JOIN goal ON player.id = goal.player_id where player.name = $1'+
            ' GROUP BY player.name'+
            ' ORDER BY goals DESC', i['name']))
    rows_players = list(set(rows_players))
    rows_players.sort(key=lambda x: x['goals'], reverse=True)
    players = []
    for i in rows_players:
        if i['goals'] != 0:
            players.append(types.InlineKeyboardButton(text=str(i['name']), callback_data=str(i['name'])))
    tverd = types.InlineKeyboardButton(text='Твердохлеб Глеб', callback_data='tverd')
    main = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main')
    for i in players:
        players_markup.add(i)
    players_markup.add(main)
    return players_markup


# message handlers

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Привет, дружочек, ты находишься в главном меню.', reply_markup=main_markup)

@dp.message_handler()
async def echo_message(message: types.Message):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    rows_names = []
    for i in range(1,48):
        rows_names.append(await db_connect.fetchrow('select name from player where id = $1', i))
    rows_names = list(set(rows_names))
    # rows_names.sort(key=lambda x: x['name'], reverse=True)
    for i in rows_names:
        input = i['name']
        if message.text == input:
            rows = await db_connect.fetchrow('SELECT player.name, COUNT(goal.player_id) as goals'+
                ' FROM player'+
                ' LEFT JOIN goal ON player.id = goal.player_id where player.name = $1'+
                ' GROUP BY player.name'+
                ' ORDER BY goals DESC', input)
            rows_assist = await db_connect.fetchrow(
                'SELECT player.name, COUNT(assist.player_id) as assists'+
                ' FROM player'+
                ' LEFT JOIN assist ON player.id = assist.player_id where player.name = $1'+
                ' GROUP BY player.name'+
                ' ORDER BY assists DESC', input)
            final = 'Имя: ' + rows_assist['name'] + '\nГолов: ' + str(rows['goals']) + ',\nАссистов: ' + str(rows_assist['assists']) + '.\n'
            await message.answer(final, reply_markup=await get_players())
    if message.text == 'Вернуться в главное меню':
        await message.answer('Ты вернулся в главное меню.', reply_markup=main_markup)
    elif message.text == 'Сезоны':
        await message.answer('Выбирай сезон.', reply_markup=seasons_markup)
    elif message.text == 'Вернуться в меню сезонов':
        await message.answer('Выбирай сезон.', reply_markup=seasons_markup)
    elif message.text == 'ШПЛ16':
        await message.answer('ШПЛ16.\nЧто интересует?', reply_markup=set_season('shpl16_champ', 'shpl16_cup', 'shpl16_top'))
    elif message.text == 'ШПЛ17':
        await message.answer('ШПЛ17.\nЧто интересует?', reply_markup=set_season('shpl17_champ', 'shpl17_cup', 'shpl17_top'))
    elif message.text == 'ШПЛ4':
        await message.answer('ШПЛ4.\nЧто интересует?', reply_markup=set_season('shpl4_champ', 'shpl4_cup', 'shpl4_top'))
    elif message.text == 'БХШПЛ':
        await message.answer('БХШПЛ.\nЧто интересует?', reply_markup=set_season('bhshpl_champ', 'bhshpl_cup', 'bhshpl_top'))
    elif message.text == 'БХШПЛ1':
        await message.answer('БХШПЛ1.\nЧто интересует?', reply_markup=set_season('bhshpl1_champ', 'bhshpl11_cup', 'bhshpl1_top'))
    elif message.text == 'Игроки':
        await message.answer('Выбирай своего кумира и смотри его статистику.', reply_markup=await get_players())
    elif message.text == 'Карточки':
        await message.answer('В режиме разработки.', reply_markup=main_markup)
    elif  message.text == 'Игры':
        await message.answer('Игры пока в режиме разработки, жди обновлений, братишка.', reply_markup=main_markup)
    elif message.text == 'Стикеры':
        await message.answer('Стикеры пока в режиме разработки, жди обновлений, братишка.', reply_markup=main_markup)
    # else:
    #     await message.answer('Я зря кнопки делал?', reply_markup=main_markup)


# callbacks

@dp.callback_query_handler(text='main')
async def main_menu(call: types.CallbackQuery):
    await call.message.answer('Ты вернулся в главное меню.', reply_markup=main_markup)

@dp.callback_query_handler(text='shpl16_champ')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    teams = []
    for i in range(1,4):
        v = await db_connect.fetchrow('SELECT team.name, COUNT(game.team1_status) as victories FROM team'+
            ' LEFT JOIN game ON team.id = game.team1_id and game.specific = \'champ\' and game.draw = $2 where team.id = $1 and team.cup_id = $3'+
            ' GROUP BY team.name ORDER BY victories DESC', i, 0, 1)
        d = await db_connect.fetchrow('SELECT team.name, COUNT(game.draw) as draws FROM team'+
            ' LEFT JOIN game ON (team.id = game.team1_id or team.id = game.team2_id) and game.specific = \'champ\'  and game.draw = $2 where team.id = $1 and team.cup_id = $3'+
            ' GROUP BY team.name ORDER BY draws DESC', i, 1, 1)
        l = await db_connect.fetchrow('SELECT team.name, COUNT(game.team2_status) as losses FROM team'+
            ' LEFT JOIN game ON team.id = game.team2_id and game.specific = \'champ\' and game.draw = $2 where team.id = $1 and team.cup_id = $3'+
            ' GROUP BY team.name ORDER BY losses DESC', i, 0, 1)
        teams.append([v['name'], v['victories'], d['draws'], l['losses']])
    teams.sort(key=lambda row: 3*row[1] + 1*row[2] + 0*row[3], reverse=True)
    print(teams)
    final = 'ЧЕМПИОНАТ\n\nПОБЕДИТЕЛЬ:\n' + teams[0][0].upper() + '🏆\n\nТаблица команд:\n\n'
    for i in teams:
        final += i[0] + ':\nВ: ' + str(i[1]) + ', Н: ' + str(i[2]) + ', П: ' + str(i[3]) + ', О: ' + str(3*i[1]+1*i[2]+0*i[3]) + '.\n'
    await call.message.answer(final, reply_markup=seasons_markup)

@dp.callback_query_handler(text='shpl16_cup')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    teams = []
    for i in range(1,4):
        v = await db_connect.fetchrow('SELECT team.name, COUNT(game.team1_status) as victories FROM team'+
            ' LEFT JOIN game ON team.id = game.team1_id and game.specific = \'cup\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ORDER BY victories DESC', i, 0)
        d = await db_connect.fetchrow('SELECT team.name, COUNT(game.draw) as draws FROM team'+
            ' LEFT JOIN game ON (team.id = game.team1_id or team.id = game.team2_id) and game.specific = \'cup\'  and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ORDER BY draws DESC', i, 1)
        l = await db_connect.fetchrow('SELECT team.name, COUNT(game.team2_status) as losses FROM team'+
            ' LEFT JOIN game ON team.id = game.team2_id and game.specific = \'cup\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ORDER BY losses ', i, 0,)
        teams.append([v['name'], v['victories'], d['draws'], l['losses']])
        print([v['name'], v['victories'], d['draws'], l['losses']])
    teams.sort(key=lambda row: 3*row[1] + 1*row[2] + 0*row[3], reverse=True)
    print(teams)
    final = 'КУБОК\n\nПОБЕДИТЕЛЬ:\n' + teams[0][0].upper() + '🏆\n\nТаблица команд:\n\n'
    for i in teams:
        final += i[0] + ':\nВ: ' + str(i[1]) + ', Н: ' + str(i[2]) + ', П: ' + str(i[3]) + ', О: ' + str(3*i[1]+1*i[2]+0*i[3]) + '.\n'
    await call.message.answer(final, reply_markup=seasons_markup)

@dp.callback_query_handler(text='shpl16_top')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    rows = []
    for i in range(1,7):
        rows.append(await db_connect.fetchrow('SELECT player.name, COUNT(goal.player_id) as goals'+
        ' FROM player'+
        ' LEFT JOIN goal ON player.id = goal.player_id and player.id = $1'+
        ' GROUP BY player.name'+
        ' ORDER BY goals DESC', i))
    rows.sort(key=lambda x: x['goals'], reverse=True)
    final = 'Топ игроков:\n\n'
    for i in rows:
        final += i['name'] + ' \nГолов: ' + str(i['goals']) + '.\n\n'
    await call.message.answer(final, reply_markup=seasons_markup)

@dp.callback_query_handler(text='shpl17_champ')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    teams = []
    for i in range(4,7):
        v = await db_connect.fetchrow('SELECT team.name, COUNT(game.team1_status) as victories FROM team'+
            ' LEFT JOIN game ON team.id = game.team1_id and game.specific = \'champ\' and game.draw = $2 and team.id = $1'+
            ' GROUP BY team.name ORDER BY victories DESC', i, 0)
        d = await db_connect.fetchrow('SELECT team.name, COUNT(game.draw) as draws FROM team'+
            ' LEFT JOIN game ON (team.id = game.team1_id or team.id = game.team2_id) and game.specific = \'champ\'  and game.draw = $2 and team.id = $1'+
            ' GROUP BY team.name ORDER BY draws DESC', i, 1)
        l = await db_connect.fetchrow('SELECT team.name, COUNT(game.team2_status) as losses FROM team'+
            ' LEFT JOIN game ON team.id = game.team2_id and game.specific = \'champ\' and game.draw = $2 and team.id = $1'+
            ' GROUP BY team.name ORDER BY losses DESC', i, 0,)
        teams.append([v['name'], v['victories'], d['draws'], l['losses']])
    teams.sort(key=lambda row: 3*row[1] + 1*row[2] + 0*row[3], reverse=True)
    print(teams)
    final = 'ЧЕМПИОНАТ\n\nПОБЕДИТЕЛЬ:\n' + teams[0][0].upper() + '🏆\n\nТаблица команд:\n\n'
    for i in teams:
        final += i[0] + ':\nВ: ' + str(i[1]) + ', Н: ' + str(i[2]) + ', П: ' + str(i[3]) + ', О: ' + str(3*i[1]+1*i[2]+0*i[3]) + '.\n'
    await call.message.answer(final, reply_markup=seasons_markup)

@dp.callback_query_handler(text='shpl17_cup')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    teams = []
    for i in range(4,7):
        v = await db_connect.fetchrow('SELECT team.name, COUNT(game.team1_status) as victories FROM team'+
            ' LEFT JOIN game ON team.id = game.team1_id and game.specific = \'cup\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ORDER BY victories DESC', i, 0)
        print(await db_connect.fetchrow('SELECT team.name, COUNT(game.team1_status) as victories FROM team'+
            ' LEFT JOIN game ON team.id = game.team1_id and game.specific = \'cup\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ORDER BY victories DESC', i, 0))
        d = await db_connect.fetchrow('SELECT team.name, COUNT(game.draw) as draws FROM team'+
            ' LEFT JOIN game ON (team.id = game.team1_id or team.id = game.team2_id) and game.specific = \'cup\'  and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ORDER BY draws DESC', i, 1)
        print(await db_connect.fetchrow('SELECT team.name, COUNT(game.draw) as draws FROM team'+
            ' LEFT JOIN game ON (team.id = game.team1_id or team.id = game.team2_id) and game.specific = \'cup\'  and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ORDER BY draws DESC', i, 1))
        l = await db_connect.fetchrow('SELECT team.name, COUNT(game.team2_status) as losses FROM team'+
            ' LEFT JOIN game ON team.id = game.team2_id and game.specific = \'cup\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ORDER BY losses DESC', i, 0,)
        print(await db_connect.fetchrow('SELECT team.name, COUNT(game.team2_status) as losses FROM team'+
            ' LEFT JOIN game ON team.id = game.team2_id and game.specific = \'cup\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ORDER BY losses DESC', i, 0,))
        teams.append([v['name'], v['victories'], d['draws'], l['losses']])
    teams.sort(key=lambda row: 3*row[1] + 1*row[2] + 0*row[3], reverse=True)
    print(teams)
    final = 'КУБОК\n\nПОБЕДИТЕЛЬ:\n' + teams[0][0].upper() + '🏆\n\nТаблица команд:\n\n'
    for i in teams:
        final += i[0] + ':\nВ: ' + str(i[1]) + ', Н: ' + str(i[2]) + ', П: ' + str(i[3]) + ', О: ' + str(3*i[1]+1*i[2]+0*i[3]) + '.\n'
    await call.message.answer(final, reply_markup=seasons_markup)

@dp.callback_query_handler(text='shpl17_top')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    rows = []
    rows_assist = []
    for i in range(8,15):
        rows.append(await db_connect.fetchrow('SELECT player.name, COUNT(goal.player_id) as goals'+
            ' FROM player'+
            ' LEFT JOIN goal ON player.id = goal.player_id and player.id = $1'+
            ' GROUP BY player.name'+
            ' ORDER BY goals DESC', i))
        rows_assist.append(await db_connect.fetchrow(
            'SELECT player.name, COUNT(assist.player_id) as assists'+
            ' FROM player'+
            ' LEFT JOIN assist ON player.id = assist.player_id and player.id = $1'+
            ' GROUP BY player.name'+
            ' ORDER BY assists DESC', i))
    print(rows)
    print(rows_assist)
    rows.sort(key=lambda x: x['goals'], reverse=True)
    final = 'Топ игроков:\n\n'
    print(rows)
    for i in rows:
        for j in rows_assist:
            if i['name'] == j['name']:
                final += i['name'] + ' \nГолов: ' + str(i['goals']) + ', Ассистов: ' + str(j['assists']) + '.\n\n'
    await call.message.answer(final, reply_markup=seasons_markup)

@dp.callback_query_handler(text='shpl4_champ')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    teams = []
    for i in range(7,11):
        v = await db_connect.fetchrow('SELECT team.name, COUNT(game.team1_status) as victories FROM team'+
            ' LEFT JOIN game ON team.id = game.team1_id and game.specific = \'champ\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ', i, 0)
        d = await db_connect.fetchrow('SELECT team.name, COUNT(game.draw) as draws FROM team'+
            ' LEFT JOIN game ON (team.id = game.team1_id or team.id = game.team2_id) and game.specific = \'champ\'  and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ', i, 1)
        l = await db_connect.fetchrow('SELECT team.name, COUNT(game.team2_status) as losses FROM team'+
            ' LEFT JOIN game ON team.id = game.team2_id and game.specific = \'champ\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ', i, 0,)
        teams.append([v['name'], v['victories'], d['draws'], l['losses']])
    teams.sort(key=lambda row: 3*row[1] + 1*row[2] + 0*row[3], reverse=True)
    print(teams)
    final = 'ЧЕМПИОНАТ\n\nПОБЕДИТЕЛЬ:\n' + teams[0][0].upper() + '🏆\n\nТаблица команд:\n\n'
    for i in teams:
        if 3*i[1]+1*i[2]+0*i[3] != 0:
            final += i[0] + ':\nВ: ' + str(i[1]) + ', Н: ' + str(i[2]) + ', П: ' + str(i[3]) + ', О: ' + str(3*i[1]+1*i[2]+0*i[3]) + '.\n'
    await call.message.answer(final, reply_markup=seasons_markup)

@dp.callback_query_handler(text='shpl4_cup')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    teams = []
    for i in range(7,11):
        v = await db_connect.fetchrow('SELECT team.name, COUNT(game.team1_status) as victories FROM team'+
            ' LEFT JOIN game ON team.id = game.team1_id and game.specific = \'cup\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ', i, 0)
        d = await db_connect.fetchrow('SELECT team.name, COUNT(game.draw) as draws FROM team'+
            ' LEFT JOIN game ON (team.id = game.team1_id or team.id = game.team2_id) and game.specific = \'cup\'  and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ', i, 1)
        l = await db_connect.fetchrow('SELECT team.name, COUNT(game.team2_status) as losses FROM team'+
            ' LEFT JOIN game ON team.id = game.team2_id and game.specific = \'cup\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ', i, 0,)
        teams.append([v['name'], v['victories'], d['draws'], l['losses']])
    teams.sort(key=lambda row: 3*row[1] + 1*row[2] + 0*row[3], reverse=True)
    print(teams)
    final = 'КУБОК\n\nПОБЕДИТЕЛЬ:\n' + teams[0][0].upper() + '🏆\n\nТаблица команд:\n\n'
    for i in teams:
        final += i[0] + ':\nВ: ' + str(i[1]) + ', Н: ' + str(i[2]) + ', П: ' + str(i[3]) + ', О: ' + str(3*i[1]+1*i[2]+0*i[3]) + '.\n'
    await call.message.answer(final, reply_markup=seasons_markup)

@dp.callback_query_handler(text='shpl4_top')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    rows = []
    for i in range(16,26):
        rows.append(await db_connect.fetchrow('SELECT player.name, COUNT(goal.player_id) as goals'+
        ' FROM player'+
        ' LEFT JOIN goal ON player.id = goal.player_id and player.id = $1'+
        ' GROUP BY player.name'+
        ' ORDER BY goals DESC', i))
    rows_assist = []
    for i in range(16,26):
        rows_assist.append(await db_connect.fetchrow(
        'SELECT player.name, COUNT(assist.player_id) as assists'+
        ' FROM player'+
        ' LEFT JOIN assist ON player.id = assist.player_id and player.id = $1'+
        ' GROUP BY player.name'+
        ' ORDER BY assists DESC', i))
    print(rows)
    print(rows_assist)
    rows.sort(key=lambda x: x['goals'], reverse=True)
    final = 'Топ игроков:\n\n'
    print(rows)
    for i in rows:
        for j in rows_assist:
            if i['name'] == j['name'] and i['goals'] != 0 and j['assists'] != 0:
                final += i['name'] + ' \nГолов: ' + str(i['goals']) + ', Ассистов: ' + str(j['assists']) + '.\n\n'
    await call.message.answer(final, reply_markup=seasons_markup)

@dp.callback_query_handler(text='bhshpl_champ')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    teams = []
    for i in range(11,18):
        v = await db_connect.fetchrow('SELECT team.name, COUNT(game.team1_status) as victories FROM team'+
            ' LEFT JOIN game ON team.id = game.team1_id and game.specific = \'champ\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ', i, 0)
        d = await db_connect.fetchrow('SELECT team.name, COUNT(game.draw) as draws FROM team'+
            ' LEFT JOIN game ON (team.id = game.team1_id or team.id = game.team2_id) and game.specific = \'champ\'  and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ', i, 1)
        l = await db_connect.fetchrow('SELECT team.name, COUNT(game.team2_status) as losses FROM team'+
            ' LEFT JOIN game ON team.id = game.team2_id and game.specific = \'champ\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ', i, 0,)
        teams.append([v['name'], v['victories'], d['draws'], l['losses']])
    teams.sort(key=lambda row: 3*row[1] + 1*row[2] + 0*row[3], reverse=True)
    print(teams)
    final = 'ЧЕМПИОНАТ\n\nПОБЕДИТЕЛЬ:\n' + teams[0][0].upper() + '🏆\n\nТаблица команд:\n\n'
    for i in teams:
        final += i[0] + ':\nВ: ' + str(i[1]) + ', Н: ' + str(i[2]) + ', П: ' + str(i[3]) + ', О: ' + str(3*i[1]+1*i[2]+0*i[3]) + '.\n'
    await call.message.answer(final, reply_markup=seasons_markup)

@dp.callback_query_handler(text='bhshpl_cup')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    teams = []
    for i in range(11,18):
        v = await db_connect.fetchrow('SELECT team.name, COUNT(game.team1_status) as victories FROM team'+
            ' LEFT JOIN game ON team.id = game.team1_id and game.specific = \'cup\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ', i, 0)
        d = await db_connect.fetchrow('SELECT team.name, COUNT(game.draw) as draws FROM team'+
            ' LEFT JOIN game ON (team.id = game.team1_id or team.id = game.team2_id) and game.specific = \'cup\'  and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ', i, 1)
        l = await db_connect.fetchrow('SELECT team.name, COUNT(game.team2_status) as losses FROM team'+
            ' LEFT JOIN game ON team.id = game.team2_id and game.specific = \'cup\' and game.draw = $2 where team.id = $1'+
            ' GROUP BY team.name ', i, 0,)
        teams.append([v['name'], v['victories'], d['draws'], l['losses']])
    teams.sort(key=lambda row: 3*row[1] + 1*row[2] + 0*row[3], reverse=True)
    print(teams)
    final = 'КУБОК\n\nПОБЕДИТЕЛЬ:\n' + teams[0][0].upper() + '🏆\n\nТаблица команд:\n\n'
    for i in teams:
        final += i[0] + ':\nВ: ' + str(i[1]) + ', Н: ' + str(i[2]) + ', П: ' + str(i[3]) + ', О: ' + str(3*i[1]+1*i[2]+0*i[3]) + '.\n'
    await call.message.answer(final, reply_markup=seasons_markup)

@dp.callback_query_handler(text='bhshpl_top')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    rows = []
    for i in range(27,46):
        rows.append(await db_connect.fetchrow('SELECT player.name, COUNT(goal.player_id) as goals'+
        ' FROM player'+
        ' LEFT JOIN goal ON player.id = goal.player_id and player.id = $1'+
        ' GROUP BY player.name'+
        ' ORDER BY goals DESC', i))
    rows_assist = []
    for i in range(27,46):
        rows_assist.append(await db_connect.fetchrow(
        'SELECT player.name, COUNT(assist.player_id) as assists'+
        ' FROM player'+
        ' LEFT JOIN assist ON player.id = assist.player_id and player.id = $1'+
        ' GROUP BY player.name'+
        ' ORDER BY assists DESC', i))
    rows.sort(key=lambda x: x['goals'], reverse=True)
    final = 'Топ игроков:\n\n'
    for i in rows:
        for j in rows_assist:
            if i['name'] == j['name'] and i['goals'] != 0 and j['assists'] != 0:
                final += i['name'] + ' \nГолов: ' + str(i['goals']) + ', Ассистов: ' + str(j['assists']) + '.\n\n'
    await call.message.answer(final, reply_markup=seasons_markup)

@dp.callback_query_handler(text='bhshpl1_champ')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    rows = await db_connect.fetchrow('SELECT name FROM player')
    print(await db_connect.fetchrow('SELECT name FROM player'))
    # for i in lst:
    #     rows.append(await db_connect.fetchrow('SELECT name FROM player'))
    str = ''
    # for i in rows:
    str +=  rows['name'] + '\n'
    await call.message.answer(str, reply_markup=seasons_markup)

@dp.callback_query_handler(text='bhshpl1_cup')
async def main_menu(call: types.CallbackQuery):
    db_connect = await asyncpg.connect(user=USER, password=PASSWORD, database=DB, host=HOST)
    rows = await db_connect.fetchrow('SELECT name FROM player')
    print(await db_connect.fetchrow('SELECT name FROM player'))
    # for i in lst:
    #     rows.append(await db_connect.fetchrow('SELECT name FROM player'))
    str = ''
    # for i in rows:
    str +=  rows['name'] + '\n'
    await call.message.answer(str, reply_markup=seasons_markup)


# polling

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)