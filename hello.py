import telebot
import config
import random
import mood
import os

from telebot import types
from mood import Mood, Callback_inline

bot = telebot.TeleBot(config.TOKEN)
decor_singer = []
decor_mood = []



def base(mes):
    global decor_singer, decor_mood
    if len(decor_mood) != 0:
        return


    arr_ns = open('static/singer_names.txt', 'r', encoding='utf-8')
    for name_sing in arr_ns:
        decor_singer.append(name_sing.strip())
    #print(decor_singer)

    arr_nm = open('static/themes.txt', 'r', encoding='utf-8')
    for name_theme in arr_nm:
     #   print(name_theme)
        now = name_theme.strip().split()[-1]
        #print(now)
        decor_mood.append(now)

    #print(decor_mood)

@bot.message_handler(commands=['start'])
def welcome(mes):

    sti = open('static/image/image_singers/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(mes.chat.id, sti)

    base(mes)
    #print(decor_mood, decor_singer)
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=4)
    item1 = types.KeyboardButton("💃 Тяночка") #"💃 Тяночка" "/start"
    item2 = types.KeyboardButton("👨‍🎤 Исполнители") #"👨‍🎤 Исполнители"   "/singer"
    item3 = types.KeyboardButton("😼 Настроение") #"😼 Настроение"   "/mood"

    markup.add(item1, item2)
    markup.add(item3)

    bot.send_message(mes.chat.id, " 😋 Приветик <b>{0.first_name}</b>!\nЗдесь вы найдёте свои любимые треки! 🎶\nТелеграм канал https://t.me/darkpree".format(mes.from_user),
    parse_mode='html', reply_markup=markup)  #reply_markup=markup


@bot.message_handler(content_types=['text'])
def allocator(mes):
    #bot.send_message(mes.chat.id, "Приветик")
    if(mes.text == "💃 Тяночка"):
        welcome(mes)
    elif mes.text == "👨‍🎤 Исполнители":
        singer(mes)
    elif mes.text == "😼 Настроение":
        mood(mes)
    else:
        bot.send_message(mes.chat.id, "Ну давай не напрягайся и нажимай на кнопочки 😊")


@bot.message_handler(commands=['singer'])
def singer(mes):

    # кнопочки исполнителей

    markup = types.InlineKeyboardMarkup(row_width=3)

    pref_names = 'static/singer_names.txt'
    folder_names = open(pref_names, 'r', encoding='utf-8')

    bn = []  # button
    for nm in folder_names:
        nm = nm.strip()
        bn.append(types.InlineKeyboardButton(nm, callback_data=nm))

    markup.add(*bn)

    bot.send_message(mes.chat.id, ' 🎙  Выберите исполнителя',reply_markup=markup)


def singer_music(call, name):
    pref = 'static/music/' + name
    pref_img = 'static/image/image_singers'
    fold_name = os.listdir(pref_img)
    for nm in fold_name:
        if name in nm:
            intro = open(pref_img + '/' + nm, 'rb')
            bot.send_photo(call.message.chat.id, intro)
            break

    #intro = open(pref_img + '.jpg', 'rb')
    #bot.send_photo(call.message.chat.id, intro)

    fold = os.listdir(pref)

    for mus in fold:
        bot.send_audio(call.message.chat.id, open(pref + '/' + mus, 'rb'))


@bot.callback_query_handler(func=lambda call: call.data in decor_singer)
def callback_inline(call):
    try:
        name = call.data
        singer_music(call, name)

    except Exception as e:
        print(repr(e))


@bot.message_handler(commands=['mood'])
def mood(mes):
    Mood(mes, bot)

@bot.callback_query_handler(func=lambda call: call.data in decor_mood)
def callback_inline(call):
    #print(10000)
    Callback_inline(call, bot)

#RUN
bot.polling(none_stop=True)