import telebot
import config
import os
from random import randint, shuffle

from telebot import types

#from hello import *



def Mood(mes, bot):

    # кнопочки тем

    markup = types.InlineKeyboardMarkup(row_width=3)

    pref_names = 'static/themes.txt'
    folder_names = open(pref_names, 'r', encoding='utf-8')

    bn = []  # button
    #print(folder_names)
    for nm in folder_names:
        nm = nm.strip()
        now = nm.split(' ')
        theme_now = now[len(now) - 1]
        bn.append(types.InlineKeyboardButton(nm, callback_data=theme_now))
        #print(theme_now)

    markup.add(*bn)

    bot.send_message(mes.chat.id, '🐥 Какое сегодня у вас настроение? 🐙', reply_markup=markup)


def mood_music(call, name, bot):
    #bot.send_message(call.message.chat.id, 'asdasdasdasdas')
    pref = 'static/themes_music/' + name
    pref_img = 'static/image/image_themes'
    #print(name)
    fold_name = os.listdir(pref_img + '/' + name)
    #print(fold_name)
    arr = [ name.strip() for name in fold_name]

    intro = open(pref_img + '/' + name + '/' + arr[randint(0, len(arr) - 1)], 'rb')
    bot.send_photo(call.message.chat.id, intro)


    #intro = open(pref_img + '.jpg', 'rb')
    #bot.send_photo(call.message.chat.id, intro)

    fold_music = list(os.listdir(pref))
    shuffle(fold_music)
    #print(fold_music)
    for mus in fold_music:
        bot.send_audio(call.message.chat.id, open(pref + '/' + mus, 'rb'))



def Callback_inline(call, bot):
    #try:
    #print(10)
    name = call.data
    mood_music(call, name, bot)

    #except Exception as e:
    #    print(repr(e))