from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def for_whom():
    Menu = InlineKeyboardMarkup(row_width=2)
    inline_btn_1 = InlineKeyboardButton('Для себя', callback_data='Для себя')
    inline_btn_2 = InlineKeyboardButton('Для клиента', callback_data='Для клиента')
    Menu.insert(inline_btn_1)
    Menu.insert(inline_btn_2)
    return Menu

def purpose():
    Menu = InlineKeyboardMarkup(row_width=1)
    inline_btn_1 = InlineKeyboardButton('Для жизни', callback_data='Для жизни')
    inline_btn_2 = InlineKeyboardButton('Для инвестиций', callback_data='Для инвестиций')
    Menu.insert(inline_btn_1)
    Menu.insert(inline_btn_2)
    return Menu

def numb_rooms():
    Menu = InlineKeyboardMarkup(row_width=2)
    inline_btn_1 = InlineKeyboardButton('Студия', callback_data='Студия')
    inline_btn_2 = InlineKeyboardButton('Однокомнатная', callback_data='Однокомнатная')
    inline_btn_3 = InlineKeyboardButton('Двухкомнатная', callback_data='Двухкомнатная')
    inline_btn_4 = InlineKeyboardButton('Трёхкомнатная', callback_data='Трёхкомнатная')
    inline_btn_5 = InlineKeyboardButton('Многокомнатная', callback_data='Многокомнатная')
    Menu.insert(inline_btn_1)
    Menu.insert(inline_btn_2)
    Menu.insert(inline_btn_3)
    Menu.insert(inline_btn_4)
    Menu.insert(inline_btn_5)
    return Menu

def cost():
    Menu = InlineKeyboardMarkup(row_width=1)
    inline_btn_1 = InlineKeyboardButton('От 7 млн. руб.', callback_data='От 7 млн. руб.')
    inline_btn_2 = InlineKeyboardButton('От 15 млн. руб.', callback_data='От 15 млн. руб.')
    inline_btn_3 = InlineKeyboardButton('От 20 млн. руб.', callback_data='От 20 млн. руб.')
    Menu.insert(inline_btn_1)
    Menu.insert(inline_btn_2)
    Menu.insert(inline_btn_3)
    return Menu