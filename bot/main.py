import os
import time
from pprint import pprint

import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import ruter


def parse(msg):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                 keyboard=[
                                     [KeyboardButton(text='Show nearby stops', request_location=True)],
                                 ])

    response = 'hi...'
    is_inline = False

    if 'text' in msg:
        response = f'Send me your location so I can show you nearby stops.'
    elif 'location' in msg:
        response, stops = ruter.get_nearby_stops(msg['location'])
        inline_kb_layout = []

        for id, name in stops.items():
            inline_kb_layout.append([InlineKeyboardButton(text=name, callback_data=str(id))])

        is_inline = True
        inline_kb = InlineKeyboardMarkup(inline_keyboard=inline_kb_layout)

    user_id = msg['from']['id']

    if is_inline:
        bot.sendMessage(int(user_id), f'{response}', reply_markup=inline_kb)
    else:
        bot.sendMessage(int(user_id), f'{response}', reply_markup=markup)

    pprint(msg)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')
    departure_data = ruter.get_departures_by_id(int(query_data))

    if len(departure_data) != 0:
        bot.sendMessage(int(from_id), departure_data)
    else:
        bot.sendMessage(int(from_id), "Seems like there are no departures from this stop in near future...")


if __name__ == '__main__':
    bot = telepot.Bot(os.environ['TOKEN'])

    bot.message_loop({
        'chat': parse,
        'callback_query': on_callback_query,
    })

    while 1:
        time.sleep(10)
