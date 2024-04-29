# Импортируем нужные библиотеки
import random
import sqlite3
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import token
from users import User
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
db_session.global_init("userid.db")
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


# Эта функция отвечает за создание нового пользователя
def new_id(vkid):
    global flags
    flags[vkid] = 0


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        # Тут считываются сообщение и id пользователя
        message = event.text.lower()
        nlmsg = event.text
        vkid = event.user_id
        # Тут если id нет в словаре, то оно туда заносится
        if vkid not in flags:
            db_sess = db_session.create_session()
            user = User()
            db_sess.add(user)
            db_sess.commit()
            new_id(vkid)
        # Тут пользователь может решить продолжить играть или нет, если пользователь решит продолжить, то ему отправится
        # следующий кадр, если нет, то общение начнется почти с нуля
        if flags[vkid] == 5:
            if 'да' in message:
                flags[vkid] = 2
            if 'нет' in message:
                flags[vkid] = 1
        # Тут бот только начинает общение, но только если пользователь напишет слово 'привет' или слово 'здравствуйте'
        # (Он просто очень обидчивый)
        if ('привет' in message or 'здравствуйте' in message) and flags[vkid] == 0:
            blasthack(vkid, 'Здравствуйте, я - чат-бот, который может искать и загадывать фильмы!')
            blasthack(vkid, 'Если хотите поугадывать фильмы, то напишите "Загадывать"')
            blasthack(vkid, 'Если хотите посмотреть фильмы, то напишите "Смотреть"')
            blasthack(vkid, 'А также если вы введете секретное слово, то я отправлю вам карту, на которой будет '
                            'отмечено место, куда вы сможете отправить жалобу на меня, также эта функция есть только '
                            'у меня')
            flags[vkid] = 1
        # Тут пользователь выбирает, какой из функций бота воспользоваться
        elif (flags[vkid] == 1 or flags[vkid] == 3) and ('загадывать' in message or 'смотреть' in message):
            if 'загадывать' in message:
                blasthack(vkid, 'Запускаю функцию "Отгадай фильм по кадру"')
                flags[vkid] = 2
            if 'смотреть' in message:
                blasthack(vkid, 'Запускаю функцию "Просмотр фильмов"')
                blasthack(vkid, 'Вот список:')
                blasthack(vkid, '\n'.join(names))
                flags[vkid] = 3
        # Тут реализована функция скидывания ссылок на фильмы
        if flags[vkid] == 3 and 'смотреть' not in message:
            if nlmsg not in names:
                blasthack(vkid, 'Простите, я не знаю этот фильм')
            else:
                blasthack(vkid, flinks[names.index(nlmsg)])
        # Тут бот случайным образом выбирает кадр и отправляет его
        if flags[vkid] == 2:
            guesscadr = guess[random.randrange(len(guess))]
            send_photo(vkid, photosid[guesscadr])
            # Тут я добавил эту строку, чтобы знать, как называется фильм, а то некоторые тестировщики не могли
            # отгадать, а я не придумал ничего легче
            print(names[guesscadr - 1])
            flags[vkid] = 4
        # Тут бот отправляет сообщение о том, что пользователь отгадал фильм, а также предлагает продолжить или
        # закончить
        if flags[vkid] == 4 and names[guesscadr - 1] in nlmsg:
            blasthack(vkid, 'Верно')
            blasthack(vkid, 'Хотите продолжить?')
            flags[vkid] = 5
        # ут бот отправляет сообщение о том, что пользователь не отгадал фильм
        if (flags[vkid] == 4 and names[guesscadr - 1] not in nlmsg and 'загадывать' not in message
                and 'да' not in message):
            blasthack(vkid, 'Неверно')
