import json

from bs4 import BeautifulSoup

import requests

import telebot
from telebot import types


class Setup:

    def __init__(self) -> None:
        self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    __mmenu = types.KeyboardButton('Главное меню')
    __search = types.KeyboardButton('Поиск')

    def create_button(self, butt_name):
        self.button = types.KeyboardButton(butt_name)
        self.markup.add(self.button)

    def create_markup(self, add_mmenu=bool, add_search=bool):
        if add_mmenu:
            self.markup.add(self.__mmenu)
        if add_search:
            self.markup.add(self.__search)
        return self.markup

    def clear_markup(self):
        del self.markup


PATH = "X:/projects/Avito_Apartment_Parser/API_KEY.json"

with open(PATH, 'r') as f:
    data = json.loads(f.read())

TELEGRAM_API_KEY = data['KEYS']['TELEGRAM']

bot = bot = telebot.TeleBot(TELEGRAM_API_KEY)


def choise_number_rooms(setup, chat_id, mes_text):
    setup.create_button('Однушка')
    setup.create_button('Двушка')
    setup.create_button('Трешка')
    markup = setup.create_markup(True, False)
    setup.clear_markup()
    bot.send_message(chat_id, text=mes_text, reply_markup=markup)


def choise_city(setup, chat_id, mes_text):
    setup.create_button('Москва')
    setup.create_button('Санкт-Петербург')
    markup = setup.create_markup(True, False)
    setup.clear_markup()
    bot.send_message(chat_id, text=mes_text, reply_markup=markup)


def main_menu(setup, chat_id, mes_text):
    setup.create_button('Сменить город')
    setup.create_button('Выбрать кол. комнат')
    markup = setup.create_markup(False, True)
    setup.clear_markup()
    bot.send_message(chat_id, text=mes_text, reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    setup = Setup()
    main_menu(setup, message.chat.id, 'Привет! Выбранный город: Москва.')


@bot.message_handler(content_types=['text'])
def bot_message(message):
    setup = Setup()
    chat_id = message.chat.id
    if message.chat.type == 'private':
        match message.text:
            case 'Выбрать кол. комнат':
                choise_number_rooms(setup, chat_id, 'Выберете кол. комнат')
            case 'Сменить город':
                choise_city(setup, chat_id, 'Выберете город')
            case 'Главное меню':
                main_menu(setup, chat_id, 'Главное меню')
            case 'Однушка':
                pass
            case 'Двушка':
                pass
            case 'Трешка':
                pass
            case 'Москва':
                pass
            case 'Санкт-Петербург':
                pass


bot.polling()
