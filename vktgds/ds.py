# Импортируем нужные библиотеки
import random
import discord
import logging
from config import bot_token


# Открываем файл со ссылками на фильмы и считываем
links = open('films.txt', 'r', encoding='Utf-8')
links = ''.join(links.readlines()).split(',\n')
flinks = []
# Разделяем ссылки и названия фильмов
for link in links:
    flinks.append(link.split(': '))
names = []
for name in flinks:
    names.append(name[0])
moment = 0
guesscadr = 0
# Создаем список, из которого потом будем брать элементы
guess = [i for i in range(1, 51)]
file = open('dsphotos.txt', 'r')
file = ' '.join(' '.join(''.join(file.readlines()).split('\n')).split('\t')).split()[1::2]
bot_messages = ['здравствуйте, я - чат-бот, который может искать и загадывать фильмы!',
                'если хотите поугадывать фильмы, то напишите "загадывать"',
                'если хотите посмотреть фильмы, то напишите "смотреть"', 'запускаю функцию "отгадай фильм по кадру"',
                'вот список:', 'простите, я не знаю этот фильм', 'верно', 'хотите продолжить?', 'неверно']


async def send_msg(message, text):
    await message.channel.send(text)


async def send_image(message, photo):
    emb = discord.Embed(title="Cadr", colour=discord.Colour.dark_green())
    emb.set_image(url=photo)
    await message.channel.send(embed=emb)


class YLBotClient(discord.Client):
    async def on_message(self, message):
        global moment, guesscadr
        msg = message.content.lower()
        nlmsg = message.content
        if msg in bot_messages:
            msg = ''
            nlmsg = ''
        if moment == 5:
            if 'да' in message:
                moment = 3
            else:
                moment = 1
        if 'привет' in msg and moment == 0:
            await send_msg(message, 'Здравствуйте, я - чат-бот, который может искать и загадывать фильмы!')
            await send_msg(message, 'Если хотите поугадывать фильмы, то напишите "Загадывать"')
            await send_msg(message, 'Если хотите посмотреть фильмы, то напишите "Смотреть"')
            moment = 1
        elif (moment == 1 and ('загадывать' in msg or 'смотреть' in msg) and 'привет' not in msg
              and 'здравствуйте' not in msg):
            if 'загадывать' in msg:
                await send_msg(message, 'Запускаю функцию "Отгадай фильм по кадру"')
                moment = 3
            if 'смотреть' in msg and 'напишите' not in msg:
                await send_msg(message, 'Запускаю функцию "Просмотр фильмов"')
                await send_msg(message, 'Вот список:')
                await send_msg(message, '\n'.join(names))
                moment = 2
        if moment == 2:
            if nlmsg.split()[1] in names:
                await send_msg(message, flinks[names.index(nlmsg.split()[1])][1])
            elif nlmsg not in names and 'простите' not in msg and 'смотреть' not in msg:
                await send_msg(message, 'Простите, я не знаю этот фильм')
        if moment == 3 and msg != '':
            guesscadr = guess[random.randrange(len(guess))]
            while guesscadr == 40 or guesscadr == 44 or guesscadr == 48:
                guesscadr = guess[random.randrange(len(guess))]
            await send_image(message, file[guesscadr - 1])
            print(names[guesscadr - 1])
            moment = 4
        if moment == 4 and names[guesscadr - 1] in nlmsg:
            await send_msg(message, 'Верно')
            await send_msg(message, 'Хотите продолжить?')
            moment = 5
        if moment == 4 and names[guesscadr - 1] not in nlmsg and msg != '':
            await send_msg(message, 'Неверно')


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
TOKEN = bot_token
intents = discord.Intents.default()
intents.members = True
client = YLBotClient(intents=intents)
client.run(TOKEN)
