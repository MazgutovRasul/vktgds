import logging
import requests
import telebot
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN
import random
from vktgds import db_sess
from vktgds.user import User


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
bot = telebot.TeleBot(BOT_TOKEN)
logger = logging.getLogger(__name__)
links = open('films.txt', 'r', encoding='Utf-8')
links = ''.join(links.readlines()).split(',\n')
flinks = []
for link in links:
    flinks.append(link.split(': '))
names = []
users = {}
for name in flinks:
    names.append(name[0])
guess = [i for i in range(1, 51)]
guesscadr = 0
db_sess.global_init("usertgid.db")


async def new_id(id):
    users[id] = [False, False, False, False, False]


def send_msg(id, text):
    bot.send_message(id, text)


def send_photo(id, photo):
    bot.send_photo(id, photo)


async def new_id(id):
    global users
    users[id] = [False, False, False, False, False]


def get_map():
    coord = '50.606802,55.364908'
    url = 'https://static-maps.yandex.ru/1.x/'
    params = {'l': 'map', 'll': coord, 'size': '650,450', 'pt': coord + ',pm2rdm', 'z': 17}
    response = requests.request('get', url, params=params)
    if response.status_code == 200:
        with open('res.png', 'wb') as file:
            file.write(response.content)
            return True
    else:
        return False


async def echo(update, context):
    global users, guesscadr
    message = update.message.text
    tgid = update.message.from_user.id
    if tgid not in users:
        db_ses = db_sess.create_session()
        user = User()
        db_ses.add(user)
        db_ses.commit()
        await new_id(tgid)
    if users[tgid][0] and users[tgid][1] and users[tgid][2] and users[tgid][3] and users[tgid][4]:
        if 'да' in message:
            users[tgid][3], users[tgid][4] = False, False
        else:
            users[tgid][1], users[tgid][2], users[tgid][3], users[tgid][4] = False, False, False, False
    if ('привет' in message.lower() or 'здравствуйте' in message.lower()) and not users[tgid][0]:
        send_msg(tgid, 'Здравствуйте, я - чат-бот, который может искать и загадывать фильмы!')
        send_msg(tgid, 'Если хотите поугадывать фильмы, то напишите "Загадывать"')
        send_msg(tgid, 'Если хотите посмотреть фильмы, то напишите "Смотреть"')
        send_msg(tgid, 'А также если вы введете секретное слово, то я отправлю вам карту, на которой будет '
                       'отмечено место, куда вы сможете отправить жалобу на меня, также эта функция есть только '
                       'у меня')
        users[tgid][0] = True
    if users[tgid][0] and 'синхрофазотрон' in message.lower():
        get_map()
        photo = open('res.png', 'rb')
        send_photo(tgid, photo)
    elif users[tgid][0] and not users[tgid][1] and ('загадывать' in message.lower() or 'смотреть' in message.lower()):
        if 'загадывать' in message.lower():
            send_msg(tgid, 'Запускаю функцию "Отгадай фильм по кадру"')
            users[tgid][1] = True
            users[tgid][2] = True
        if 'смотреть' in message.lower():
            send_msg(tgid, 'Запускаю функцию "Просмотр фильмов"')
            send_msg(tgid, 'Вот список:')
            send_msg(tgid, '\n'.join(names))
            users[tgid][1] = False
            users[tgid][2] = True
    if users[tgid][0] and not users[tgid][1] and users[tgid][2] and 'смотреть' not in message.lower():
        if message not in names:
            send_msg(tgid, 'Простите, я не знаю этот фильм')
        else:
            send_msg(tgid, flinks[names.index(message)][1])
    if users[tgid][0] and users[tgid][1] and users[tgid][2] and not users[tgid][3]:
        guesscadr = guess[random.randrange(len(guess))]
        photo = open('photos/' + str(guesscadr + 1) + '.webp', 'rb')
        send_photo(tgid, photo)
        users[tgid][3] = True
        print(names[guesscadr])
    if (users[tgid][0] and users[tgid][1] and users[tgid][2] and users[tgid][3] and names[guesscadr].lower() in
            message.lower() and 'загадывать' not in message.lower()):
        send_msg(tgid, 'Верно')
        send_msg(tgid, 'Хотите продолжить?')
        users[tgid][4] = True
    elif (users[tgid][0] and users[tgid][1] and users[tgid][2] and users[tgid][3] and not names[guesscadr] in message
          and 'загадывать' not in message.lower() and 'да' not in message.lower()):
        send_msg(tgid, 'Неверно')


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
