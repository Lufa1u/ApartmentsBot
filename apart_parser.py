import json

from bs4 import BeautifulSoup

import requests

import telebot
from telebot import types


PATH = "X:/projects/Avito_Apartment_Parser/API_KEY.json"

with open(PATH, 'r') as f:
    data = json.loads(f.read())

TELEGRAM_API_KEY = data['KEYS']['TELEGRAM']

bot = bot = telebot.TeleBot(TELEGRAM_API_KEY)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Сменить город')
    button2 = types.KeyboardButton('Выбрать кол. комнат')
    markup.add(button1, button2)
    bot.send_message(
        message.chat.id,
        text='Привет! Выбранный город: Москва. Что будем искать?',
        reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    'https://www.avito.ru/moskva/nedvizhimost'
    if message.chat.type == 'private':
        match message.text:
            case 'Выбрать кол. комнат':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = types.KeyboardButton('Однушка')
                button2 = types.KeyboardButton('Двушка')
                button3 = types.KeyboardButton('Трешка')
                main_menu = types.KeyboardButton('Главное меню')
                markup.add(button1, button2, button3, main_menu)
                bot.send_message(
                    message.chat.id, text='Выбрать кол. комнат',
                    reply_markup=markup)
            case 'Сменить город':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = types.KeyboardButton('Москва')
                button2 = types.KeyboardButton('Санкт-Петербург')
                main_menu = types.KeyboardButton('Главное меню')
                markup.add(button1, button2, main_menu)
                bot.send_message(
                    message.chat.id, text='Сменить город', reply_markup=markup)
            case 'Главное меню':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = types.KeyboardButton('Сменить город')
                button2 = types.KeyboardButton('Выбрать кол. комнат')
                markup.add(button1, button2)
                bot.send_message(
                    message.chat.id, text='Что будем искать?',
                    reply_markup=markup)
            case 'Однушка':
                pass
            case 'Двушка':
                pass
            case 'Трешка':
                pass
            case 'Москва':
                city = 'moskva'
                url = 'https://www.avito.ru/' + city + '/nedvizhimost'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = types.KeyboardButton(
                    'Найти самые выгодные предложения')
                main_menu = types.KeyboardButton('Главное меню')
                markup.add(button1, main_menu)
                bot.send_message(
                    message.chat.id, text='Выбран город: Москва',
                    reply_markup=markup)
            case 'Санкт-Петербург':
                city = 'sankt-peterburg'
                url = 'https://www.avito.ru/' + city + '/nedvizhimost'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = types.KeyboardButton(
                    'Найти самые выгодные предложения')
                main_menu = types.KeyboardButton('Главное меню')
                markup.add(button1, main_menu)
                bot.send_message(
                    message.chat.id, text='Выбран город: Санкт-Петербург',
                    reply_markup=markup)
            case 'Найти самые выгодные предложения':
                pass


bot.polling()
