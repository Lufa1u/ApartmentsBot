import json

from ParserAvito import search_apart

import telebot
from telebot import types


PATH = "X:/projects/Avito_Apartment_Parser/API_KEY.json"

with open(PATH, 'r') as f:
    data = json.loads(f.read())

TELEGRAM_API_KEY = data['KEYS']['TELEGRAM']

bot = telebot.TeleBot(TELEGRAM_API_KEY)


class BotSettings:

    def __init__(self):
        self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    city = 'moskva'
    rooms = ''
    all_var = '-ASgBAgICAkSSA8gQ8AeQUg'

    __mmenu = types.KeyboardButton('Главное меню')
    __search = types.KeyboardButton('Поиск')

    def create_url(self):
        BotSettings.url = f'https://www.avito.ru/{self.city}/kvartiry/sdam/na_dlitelnyy_srok{self.rooms}{self.all_var}'
        return self.url

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

    def search(self, chat_id, url):
        bot.send_message(
            chat_id, 'Поиск подходящих квартир займет не больше пяти минут, ожидайте сообщения от бота.')
        mes_text = search_apart(url)
        bot.send_message(chat_id, mes_text)

    def main_menu(self, chat_id, mes_text):
        self.create_button('Настройки')
        markup = self.create_markup(False, True)
        self.clear_markup()
        bot.send_message(chat_id, mes_text, reply_markup=markup)

    def settings(self, chat_id, mes_text):
        self.create_button('Выбрать город')
        self.create_button('Выбрать планировку')
        markup = self.create_markup(True, False)
        self.clear_markup()
        bot.send_message(chat_id, mes_text, reply_markup=markup)

    def choise_city(self, chat_id, mes_text):
        self.create_button('Москва')
        self.create_button('Санкт-Петербург')
        markup = self.create_markup(True, False)
        self.clear_markup()
        bot.send_message(chat_id, mes_text, reply_markup=markup)

    def choise_layout(self, chat_id, mes_text):
        self.create_button('Студия')
        self.create_button('Одна-комнатная')
        self.create_button('Двух-комнатная')
        self.create_button('Трех-комнатная')
        self.create_button('Все варианты')
        markup = self.create_markup(True, False)
        self.clear_markup()
        bot.send_message(chat_id, mes_text, reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    hello_message = 'Привет, этот бот поможет снять тебе квартиру по самой низкой цене!\n\n' + \
        'Сейчас выставлены стандартные настройки для поиска:\n' + 'Все варианты в городе Москва\n\n' + \
        'Вы можете изменить их во вкладке "Настройки"'
    BotSettings.city = 'moskva'
    BotSettings.rooms = ''
    BotSettings.all_var = '-ASgBAgICAkSSA8gQ8AeQUg'
    setup = BotSettings()
    setup.main_menu(message.chat.id, hello_message)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    setup = BotSettings()
    chat_id = message.chat.id
    if message.chat.type == 'private':
        match message.text:
            case 'Поиск':
                url = setup.create_url()
                setup.search(chat_id, url)
            case 'Главное меню':
                setup.main_menu(chat_id, 'Главное меню')
            case 'Настройки':
                setup.settings(chat_id, 'Настройки')
            case 'Выбрать город':
                setup.choise_city(chat_id, 'Выберете город')
            case 'Выбрать планировку':
                setup.choise_layout(chat_id, 'Выберете планировку')
            case 'Студия':
                BotSettings.all_var = ''
                BotSettings.rooms = '/studii-ASgBAQICAkSSA8gQ8AeQUgFAzAgUjFk'
                setup.main_menu(chat_id, 'Выбраны студии')
            case 'Одна-комнатная':
                BotSettings.all_var = ''
                BotSettings.rooms = '/1-komnatnye-ASgBAQICAkSSA8gQ8AeQUgFAzAgUjlk'
                setup.main_menu(chat_id, 'Выбрано комнат: 1')
            case 'Двух-комнатная':
                BotSettings.all_var = ''
                BotSettings.rooms = '/2-komnatnye-ASgBAQICAkSSA8gQ8AeQUgFAzAgUkFk'
                setup.main_menu(chat_id, 'Выбрано комнат: 2')
            case 'Трех-комнатная':
                BotSettings.all_var = ''
                BotSettings.rooms = '/3-komnatnye-ASgBAQICAkSSA8gQ8AeQUgFAzAgUklk'
                setup.main_menu(chat_id, 'Выбрано комнат: 3')
            case 'Все варианты':
                BotSettings.rooms = ''
                BotSettings.all_var = '-ASgBAgICAkSSA8gQ8AeQUg'
                setup.main_menu(chat_id, 'Выбраны все варианты')
            case 'Москва':
                BotSettings.city = 'moskva'
                setup.settings(chat_id, 'Выбран город: Москва')
            case 'Санкт-Петербург':
                BotSettings.city = 'sankt-peterburg'
                setup.settings(chat_id, 'Выбран город: Санкт-Петербург')


bot.polling()
