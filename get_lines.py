import datetime
import random

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import sqlite3
import requests
from telegram import ReplyKeyboardMarkup, Update
from telegram import ReplyKeyboardRemove
from telegram import KeyboardButton
from datetime import date

TOKEN = '1798183807:AAF6MpavJ0O-urpRvBa1uqicmo2nslczCPY'  # Токен бота

URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=196ed9c0c5bf90bef2fb3a1c52b6d925'  # Ссылка для
# получения информации о погоде

today = date.today()
status_horoscope, status_cities, status_events = False, False, False
button_help = 'Помоги мне!'
button_horoscope = 'Гороскоп'
button_weather = 'Погода'
button_astr_events = 'Астрологические события 2021'
button_back = 'Назад 🔙'
zodiac_sings = [['Овен', 'Телец', 'Близнецы'], ['Рак', 'Лев', 'Дева'],
                ['Весы', 'Скорпион', 'Стрелец'], ['Козерог', 'Водолей', 'Рыбы'], [button_back]]
cities = [['Вологда', 'Великий Устюг', 'Череповец'], ['Тотьма', 'Вытегра', 'Устюжна'],
          ['Шексна', 'Белозерск', 'Кириллов'], [button_back]]
comands = ['/help - Помоги мне', '/horoscope - Гороскоп', '/weather - Погода',
           '/astr_events - Астрологические события 2021']
tt = [['Сегодня', 'Завтра']]
zz = ''
first_message = False
declension_cities = {
    'Вологда': 'Вологде', 'Велкиий Устюг': 'Великом Устюге', 'Череповец': 'Череповце', 'Тотьма':
        'Тотьме', 'Вытегра': 'Вытегре', 'Устюжна': 'Устюжне', 'Шексна': 'Шексне', 'Белозерск': 'Белозерске',
    'Кириллов': 'Кириллове'
}
months_dict = {'Январь': '01', 'Февраль': '02', 'Март': '03', 'Апрель': '04', 'Май': '05', 'Июнь': '06', 'Июль': '07',
               'Август': '08', 'Сентябрь': '09', 'Октябрь': '10', 'Ноябрь': '11', 'Декабрь': '12'
               }
months = [['Январь', 'Февраль', 'Март'], ['Апрель', 'Май', 'Июнь'], ['Июль', 'Август',
          'Сентябрь'], ['Октябрь', 'Ноябрь', 'Декабрь'], [button_back]]
comands = ['/help - Помоги мне', '/horoscope - Гороскоп', '/weather - Погода',
           '/astr_events - Астрологические события 2021']
start = False

with open('horoscope1.txt', encoding="utf-8") as f1:
    a = f1.readlines()
with open('horoscope2.txt', encoding="utf-8") as f2:
    b = f2.readlines()

reply_markup_start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=button_horoscope), KeyboardButton(text=button_weather),
         KeyboardButton(text=button_astr_events)],
        [KeyboardButton(text=button_help)]],
    resize_keyboard=True)


# Main функция для запуска бота
def main():
    print('Бот запущен!')
    updater = Updater(TOKEN,
                      use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))

    updater.start_polling()
    updater.idle()


# Создание кнопки помощи
def button_help_hundler(update: Update, context: CallbackContext):
    global reply_markup_start
    update.message.reply_text(
        text='Нажми нужную кнопку или введи интересующую команду из следующего списка: \n{}'.format(
            '\n'.join(comands)
        ),
        reply_markup=reply_markup_start,
    )

# Создание кнопки для вывода гороскопа
def button_horoscope_hundler(update: Update, context: CallbackContext):
    global status_horoscope
    reply_markup = ReplyKeyboardMarkup(zodiac_sings, resize_keyboard=True)
    status_horoscope = True
    update.message.reply_text('Выберите интересующий знак зодиака',
                              reply_markup=reply_markup)


# Кнопка для вывода погоды
def button_weather_hundler(update: Update, context: CallbackContext):
    global status_cities
    status_cities = True
    reply_markup = ReplyKeyboardMarkup(cities, resize_keyboard=True)
    update.message.reply_text('Выберите город в Вологодской области, в котором вы хотели бы узнать погоду',
                              reply_markup=reply_markup)


# Создание кнопки для возвращение в начало
def button_back_hundler(update: Update, context: CallbackContext):
    global status_cities, status_horoscope
    status_cities, status_horoscope = False, False
    update.message.reply_text(
        text='Нажми нужную кнопку или введи интересующую команду из следующего списка: \n{}'.format(
            '\n'.join(comands)
        ),
        reply_markup=reply_markup_start,
    )


# Обработчик команд
def message_handler(update: Updater, context: CallbackContext):
    global first_message, zz, tt, status_events
    text = update.message.text
    if text == button_help or str(text)[1:] == 'help':
        return button_help_hundler(update=update, context=context)
    elif text == button_horoscope or str(text)[1:] == 'horoscope':
        return button_horoscope_hundler(update=update, context=context)
    elif text == button_weather or str(text)[1:] == 'weather':
        return button_weather_hundler(update=update, context=context)
    elif text == button_back:
        return button_back_hundler(update=update, context=context)
    elif text == button_astr_events:
        status_events = True
        reply_markup = ReplyKeyboardMarkup(months)
        update.message.reply_text('Выберите месяц, в котором бы вы хотели пссмотреть астрологические события',
                                  reply_markup=reply_markup)
    elif (text in months[0] or text in months[1] or text in months[2] or text in months[3]) and status_events:
        t = database(update=update, name='', key='ast', month=text)
        for i in t:
            update.message.reply_text(i[0])
    # Если пользователь написал сообщение оканчивающееся на знак вопроса
    elif update.message.text[-1] == '?':
        update.message.reply_text('Конечно можно спросить! Только я культурно промолчу... '
                                  'Лучше воспользуйся моими возможностями.')
        button_help_hundler(update=update, context=context)
    # Если человек написал утвердительное предложение
    elif update.message.text[-1] == '.':
        update.message.reply_text('Вполне возможно! Нa вкус и цвет товарищей нет ;)')
    elif not first_message or str(text)[1:] == 'start':
        first_message = True
        name = update['message']['chat']['first_name']
        familar_user = database(update=update, name=name, key='remember', month='')
        if familar_user:
            update.message.reply_text('И снова здравствуй, {}! Чем могу помочь?'.format(name),
                                      reply_markup=reply_markup_start)
        else:
            update.message.reply_text('Привет, {}! Чем могу помочь?'.format(name),
                                      reply_markup=reply_markup_start)
    # Если нужно вывести гороском по определенному знаку зодиака
    elif text in ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева',
                  'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']:
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                ['Сегодня', 'Завтра']
            ],
            resize_keyboard=True,
        )
        status_horoscope = True
        update.message.reply_text('Выбранный знак зодиака - {}. Выберите интересующий день'.format(text),
                                  reply_markup=reply_markup)
        zz = text
    elif text in tt[0]:
        if text == 'Сегодня':
            text = 'Today'
        else:
            text = 'Tomorrow'
        update.message.reply_text(horoscope_bd(update, context, text, zz))
    # Если нужно вывести погоду в каком-либо городе Вологодской области
    elif (text in cities[0] or text in cities[1] or text in cities[2]) and status_cities:
        # Отправка запроса для получения данных о погоде
        req = (requests.get(URL.format(text))).json()
        # Перевод температуры в градусы цельсия из кельвина
        wether = round(float(req['main']['temp']) - 273.15)
        update.message.reply_text(f'В {declension_cities.get(text)} сейчас {wether} градусов')
    else:
        pass


# Функция для работы с БД
def database(update: Update, name, key, month):
    # Подключение к БД
    con = sqlite3.connect('horoscope_bot_users')
    cursor = con.cursor()
    # Если нужно запомнить нужного пользователя или выдать ник старого
    if key == 'remember':
        res = cursor.execute(f"""SELECT login FROM users WHERE login = '{name}'""").fetchone()
        if res is None:
            res = cursor.execute(f"""INSERT INTO users(login) VALUES('{name}')""")
            con.commit()
            return None
        else:
            return True
    elif key == 'ast':
        res = cursor.execute(f"""SELECT name FROM events WHERE month = '{months_dict[month]}'""").fetchall()
        return res
    con.close()


def horoscope_text(day, sing):
    hp = []
    for i in range(1):
        hp.append(a[random.randrange(len(a))][:-1])
    hp.append(b[random.randrange(len(b))][:-1])
    hp = ' '.join(hp)
    return hp


def horoscope_bd(update: Update, context: CallbackContext, day, sing):
    con = sqlite3.connect('zodiac_sings.db')
    cursor = con.cursor()
    res = cursor.execute(f"""SELECT today FROM z_sings""").fetchone()
    dat_e = datetime.datetime.today().strftime("%d-%m-%Y")
    if res[0] == dat_e:
        return cursor.execute(f"""SELECT today FROM horoscope WHERE login = ?""",
                              (sing,)).fetchone()
    else:
        res = horoscope_text(day, sing)
        cursor.execute(f"""UPDATE horoscope SET today = '{res}'""").fetchone()
        cursor.execute(f"""UPDATE horoscope SET sing = '{sing}'""").fetchone()
        cursor.execute(f"""UPDATE z_sings SET today ='{dat_e}' WHERE sings = '{sing}'""").fetchone()
        con.commit()
        return res


if __name__ == '__main__':
    main()
