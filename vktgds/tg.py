import logging
import discord
import telebot
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN
import random


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
emb = discord.Embed(title = "Pepe", colour=discord.Colour.dark_green())


async def new_id(id):
    users[id] = [False, False, False, False, False]


def send_msg(id, text):
    bot.send_message(id, text)


def send_photo(id, photo):
    bot.send_photo(id, photo)


async def echo(update, context):
    global users, guesscadr
    message = update.message.text
    id = update.message.from_user.id
    if id not in users:
        await new_id(id)
    if users[id][0] and users[id][1] and users[id][2] and users[id][3] and users[id][4]:
        if 'да' in message:
            users[id][3], users[id][4] = False, False
        else:
            users[id][1], users[id][2], users[id][3], users[id][4] = False, False, False, False
    if ('привет' in message.lower() or 'здравствуйте' in message.lower()) and not users[id][0]:
        send_msg(id, 'Здравствуйте, я - чат-бот, который может искать и загадывать фильмы!')
        send_msg(id, 'Если хотите поугадывать фильмы, то напишите "Загадывать"')
        send_msg(id, 'Если хотите посмотреть фильмы, то напишите "Смотреть"')
        users[id][0] = True
    elif users[id][0] and not users[id][1] and ('загадывать' in message.lower() or 'смотреть' in message.lower()):
        if 'загадывать' in message.lower():
            send_msg(id, 'Запускаю функцию "Отгадай фильм по кадру"')
            users[id][1] = True
            users[id][2] = True
        if 'смотреть' in message.lower():
            send_msg(id, 'Запускаю функцию "Просмотр фильмов"')
            send_msg(id, 'Вот список:')
            send_msg(id, '\n'.join(names))
            users[id][1] = False
            users[id][2] = True
    if users[id][0] and not users[id][1] and users[id][2] and 'смотреть' not in message.lower():
        if message not in names:
            send_msg(id, 'Простите, я не знаю этот фильм')
        else:
            send_msg(id, flinks[names.index(message)][1])
    if users[id][0] and users[id][1] and users[id][2] and not users[id][3]:
        guesscadr = guess[random.randrange(len(guess))]
        photo = open('photos/' + str(guesscadr + 1) + '.webp', 'rb')
        send_photo(id, photo)
        users[id][3] = True
    if (users[id][0] and users[id][1] and users[id][2] and users[id][3] and names[guesscadr] in message
            and not 'загадывать' in message.lower()):
        send_msg(id, 'Верно')
        send_msg(id, 'Хотите продолжить?')
        users[id][4] = True
    if (users[id][0] and users[id][1] and users[id][2] and users[id][3] and not names[guesscadr] in message
            and not 'загадывать' in message.lower() and not 'да' in message.lower()):
        send_msg(id, 'Неверно')


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
