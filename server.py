#
# Обязательная часть:
# 1. Запустить у себя код сервера и клиентов, проверить, что сообщения отправляются и принимаются.
# 2. Дополнить метод "/status", чтобы он также возвращал общее количество пользователей и сообщений на сервере.
#
# По желанию:
# Реализовать на сервере чат-бота, который работает по ключевым словам.
#
# 1.Рефакторинг
#

import time
from datetime import datetime
from random import randint

from flask import Flask, request, abort

app = Flask(__name__)
db = [
    {
        'name': 'Nick',
        'text': 'Hello!',
        'time': time.time()
    },
    {
        'name': 'Ivan',
        'text': 'Hello, Nick!',
        'time': time.time()
    },
]


def get_randomtip():
    tip_list=[
        'Beautiful is better than ugly.',
        'Explicit is better than implicit.',
        'Simple is better than complex.',
        'Complex is better than complicated.',
        'Flat is better than nested.',
        'Sparse is better than dense.',
        'Readability counts.',
        'Special cases aren\'t special enough to break the rules.',
        'Although practicality beats purity.',
        'Errors should never pass silently.\nUnless explicitly silenced.',
        'In the face of ambiguity, refuse the temptation to guess.',
        'There should be one-- and preferably only one --obvious way to do it.',
        'Although that way may not be obvious at first unless you\'re Dutch.',
        'Now is better than never.\nAlthough never is often better than *right* now.',
        'If the implementation is hard to explain, it\'s a bad idea.\nIf the implementation is easy to explain, it may be a good idea.',
        'Namespaces are one honking great idea -- let\'s do more of those!'
    ]
    return tip_list[randint(0,len(tip_list)-1)]


bot_manual = """
Simple chat-bot available commands:
/info
/help or /? - this manual
/tip - some wise tip
/version - messenger version
"""
bot_answer={
    '/info': 'Skillbox Messenger. Flask training project. April 19-21 2021.',
    '/help': bot_manual,
    '/?': bot_manual,
    '/tip': get_randomtip(),
    '/version': '0.1.12'
}

def get_username(x):
    return x.get('name', '')


@app.route("/")
def hello():
    return "Hello, Messenger!"


@app.route("/status")
def status():
    dt = datetime.now()
    mc = len(db)  # messages count
    uc = len(set(map(get_username, db)).difference({'', 'Bot'}))  # не считаем бота за человека
    return {
        'status': True,
        'name': 'Skillbox Messenger',  # произвольное имя вашего мессенджера
        'time': time.time(),
        'dt': dt,
        'Message count': mc,
        'Unique users number': uc
        # 'time6': dt.strftime('%Y/%m/%d %H:%M')
    }


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json

    # if not isinstance(data, dict):
    #     return abort(400)
    # if 'name' not in data or 'text' not in data:
    #     return abort(400)

    try:
        name, text = str(data['name']), str(data['text'])
    except:
        return abort(400)

    # if not isinstance(name, str) or not isinstance(text, str):
    #     return abort(400)
    if name == '' or text == '':
        return abort(400)

    db.append({
        'name': name,
        'text': text,
        'time': time.time()
    })

    if text[0]=='/':
        db.append({
            'name': 'Bot',
            'text': bot_answer.get(text,'sorry, I don\'t understand this command'),
            'time': time.time()
        })

    return {'ok': True}


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    messages = []
    for message in db:
        if message['time'] > after:
            messages.append(message)

    return {'messages': messages[:50]}


app.run()
