# Импортируем нужные библиотеки
import random
import sqlite3
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import token
from users import User
from datetime import datetime
import db_session
# from yaweather import Russia, YaWeather


# Подключаемся к API вконтакте
bh = vk_api.VkApi(token=token)
give = bh.get_api()
longpoll = VkLongPoll(bh)
# Открываем файл со ссылками на фильмы и считываем
links = open('films.txt', 'r', encoding='Utf-8')
links = ''.join(links.readlines()).split(',\n')
flinks = []
db_session.global_init("userids.db")
# Разделяем ссылки и названия фильмов
for link in links:
    flinks.append(link.split(': '))
names = []
for name in flinks:
    names.append(name[0])
# Создаем список, из которого потом будем брать элементы
guess = [i for i in range(1, 51)]
# Открываем базу данных и считываем id всех фото во вконтакте
db = 'vkphotos.sqlite'
con = sqlite3.connect(db)
cur = con.cursor()
photosid = dict(cur.execute("""SELECT * FROM Photo""").fetchall())
# Эта переменная отвечает за номер выбранного элемента, когда вы отгадываете фильм
guesscadr = 0
# Этот словарь отвечает за то, чтобы сохранять то, на каком моменте общения сейчас пользователь
flags = {}


# Эта функция отвечает за отправку сообщений
def blasthack(id, text):
    bh.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


# Эта функция отвечает за отправку картинок
def send_photo(id, url):
    bh.method("messages.send",
              {"peer_id": id, "message": "Вот кадр из фильма", "attachment": url,
               "random_id": 0})


def getWeather():
    pass
    # dict_sample = {"clear": "ясно",
    #                "partly-cloudy": "малооблачно"}
    # y = YaWeather(api_key='9ba2da0e-4b76-4bb5-8ac6-f01b47c6a822')
    # res = y.forecast(Russia.Kazan)
    # print(res)
    # return f'температура: {res.fact.temp} °C, ощущается {res.fact.feels_like} °C ' + '\n'\
    #        f'на улице: {dict_sample[res.fact.condition]}'


# Эта функция отвечает за создание нового пользователя
def new_id(vkid):
    global flags
    flags[vkid] = 0


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        message = event.text.lower()
        nlmsg = event.text
        vkid = event.user_id
        if vkid not in flags:
            db = 'vkids.sqlite'
            con = sqlite3.connect(db)
            cur = con.cursor()
            length = len(dict(cur.execute(f"""SELECT * FROM vkids""").fetchall()))
            cur.execute(f"""INSERT INTO vkids Values('{str(length + 1)}', '{vkid}')""").fetchall()
            db_sess = db_session.create_session()
            user = User()
            db_sess.add(user)
            db_sess.commit()
            print('asdf')
            new_id(vkid)
        if flags[vkid] == 5:
            if 'да' in message:
                flags[vkid] = 2
            else:
                flags[vkid] = 0
        if ('привет' in message or 'здравствуйте' in message) and flags[vkid] == 0:
            blasthack(vkid, 'Здравствуйте, я - чат-бот, который может искать и загадывать фильмы!')
            blasthack(vkid, 'Если хотите поугадывать фильмы, то напишите "Загадывать"')
            blasthack(vkid, 'Если хотите посмотреть фильмы, то напишите "Смотреть"')
            flags[vkid] = 1
        elif flags[vkid] == 1 and ('загадывать' in message or 'смотреть' in message):
            if 'загадывать' in message:
                blasthack(vkid, 'Запускаю функцию "Отгадай фильм по кадру"')
                flags[vkid] = 2
            if 'смотреть' in message:
                blasthack(vkid, 'Запускаю функцию "Просмотр фильмов"')
                blasthack(vkid, 'Вот список:')
                blasthack(vkid, '\n'.join(names))
                flags[vkid] = 3
        if flags[vkid] == 3 and 'смотреть' not in message:
            if nlmsg not in names:
                blasthack(vkid, 'Простите, я не знаю этот фильм')
            else:
                blasthack(vkid, flinks[names.index(nlmsg)])
        if flags[vkid] == 2:
            guesscadr = guess[random.randrange(len(guess))]
            send_photo(vkid, photosid[guesscadr])
            flags[vkid] = 4
        if flags[vkid] == 4 and names[guesscadr - 1] in nlmsg:
            blasthack(vkid, 'Верно')
            blasthack(vkid, 'Хотите продолжить?')
            flags[vkid] = 5
        if (flags[vkid] == 4 and names[guesscadr - 1] not in nlmsg and 'загадывать' not in message
                and 'да' not in message):
            blasthack(vkid, 'Неверно')
