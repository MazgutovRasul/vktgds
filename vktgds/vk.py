import vk_api
import webbrowser
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# Создаём переменную для удобства в которой хранится наш токен от группы

token = ('vk1.a.qFLoynHldilnr5XGtcZcyjWFwjN-iqdvDP_lQjKMmPSKC2j4EQUmtShp5Aw5P9XXZXWxcPZ3RqRApCvKLWVHiZIQL-qxQLpIIkxC2Ig'
         'IFYIXoyypQKVaRjjGnVTA1x0KhYb1SjE8wZABx0K2vrGImaV5nHxtuBdVh6ZoK1KlmScWUy0rqs56PvLG2M1odiy__m8qw6LQz98tORTplVPw'
         'pw')

# Подключаем токен и longpoll
bh = vk_api.VkApi(token=token)
give = bh.get_api()
longpoll = VkLongPoll(bh)

links = open('films.txt', 'r', encoding='Utf-8')
links = ''.join(links.readlines()).split(',\n')
flinks = []
for link in links:
    flinks.append(link.split(': '))
names = []
for name in flinks:
    names.append(name[0])
users = {}


def blasthack(id, text):
    bh.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            message = event.text.lower()
            nlmsg = event.text
            id = event.user_id
            if id not in users:
                users[id] = [False]
            if ('привет' in message or 'здравствуйте' in message) and not users[id][0]:
                blasthack(id, 'Здравствуйте, я - чат-бот, который может искать фильмы! Напишите название фильма и'
                              ' я попытаюсь отправить Вам ссылку на фильм')
                blasthack(id, 'Сейчас я вам могу помочь лишь с некоторыми фильмами')
                blasthack(id, 'Вот список:')
                blasthack(id, '\n'.join(names))
                users[id][0] = True
            elif users[id][0]:
                if nlmsg not in names:
                    blasthack(id, 'Простите, я не знаю этот фильм')
                else:
                    blasthack(id, flinks[names.index(nlmsg)])
