# -*- coding: utf-8 -*-
import asyncio
import io
import logging
import time

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from db import Database
from keyboard import *

bot = Bot('5778899030:AAEgqs1LOri_YTN_xV8jkgKkD8yQpWvvEyY')
# Диспетчер для бота
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

db = Database('database.db')

class AddRecord(StatesGroup):
    purpose = State()
    numb_rooms = State()
    cost = State()
    phone = State()
    fin = State()

class Mailing(StatesGroup):
    id = State()
    status = State()
    text = State()

class MailingFile(StatesGroup):
    id = State()
    file = State()

class Call(StatesGroup):
    phone = State()

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Я виртуальный помощник Бутика новостроек RELOCX. В этом чате вы можете оформить подборку новостроек по вашим критериям. Ответьте на 3 вопроса, чтобы заказать бесплатный каталог и получить подарок.")
    try:
        db.add_user(message.from_user.id, message.from_user.username, "Не прошёл")
        await bot.send_message(-1001563476682, f"Пользователь: @{message.from_user.username} зарегестрировался")
    except:
        pass

    await message.answer(
        "Укажите цель покупки квартиры в Москве:", reply_markup=purpose())
    await AddRecord.numb_rooms.set()

@dp.callback_query_handler(state=AddRecord.numb_rooms)
async def del_records_del(callback_query: types.CallbackQuery, state: FSMContext):
    records = callback_query.data
    await state.update_data(purpose=records)
    await bot.send_message(callback_query.from_user.id, f"Укажите желаемое количество комнат:", reply_markup=numb_rooms())
    await AddRecord.cost.set()

@dp.callback_query_handler(state=AddRecord.cost)
async def del_records_del(callback_query: types.CallbackQuery, state: FSMContext):
    records = callback_query.data
    await state.update_data(numb_rooms=records)
    await bot.send_message(callback_query.from_user.id, f"Укажите ценовую категорию:", reply_markup=cost())
    await AddRecord.phone.set()


@dp.callback_query_handler(state=AddRecord.phone)
async def del_records_del(callback_query: types.CallbackQuery, state: FSMContext):
    records = callback_query.data
    await state.update_data(cost=records)
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton(
            text='Отправить номер телефона',
            request_contact=True))
    await bot.send_message(callback_query.from_user.id, f"Подборка новостроек уже формируется.\nДля корректной отправки её вам и закрепления подарка, вам необходимо отправить номер телефона.", reply_markup=markup)
    await AddRecord.fin.set()

@dp.message_handler(content_types=types.ContentType.CONTACT, state=AddRecord.fin)
async def del_records_del(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact['phone_number'])
    data = await state.get_data()
    db.update_status(message.from_user.id, "Прошёл", data['phone'])
    await bot.send_message(-1001563476682, f"""Пользователь: @{message.from_user.username}
    id: {message.from_user.id}
    status: Прошёл
    Номер телефона: {message.contact['phone_number']}
    Ответы: 
    {data['purpose']}
    {data['numb_rooms']}
    {data['cost']}""")
    await bot.send_message(message.from_user.id, "Благодарим за прохождение опроса, заканчивается вёрстка вашего каталога, в скором времени вы его получите.")
    try:
        doc = open('file.pdf', 'rb')
        await bot.send_document(message.chat.id, doc)
    except:
        pass
    await state.finish()

@dp.message_handler(commands="expert")
async def cmd_start(message: types.Message):
    await message.answer(
        "Ссылка на эксперта: @bav_bav")

@dp.message_handler(commands="call")
async def cmd_start(message: types.Message):
    await message.answer(
        "Чтобы вам перезвонили, поделитесь телефоном по кнопке. В течение 20 минут вам позвонит эксперт по недвижимости.")
    await Call.phone.set()

@dp.message_handler(content_types=types.ContentType.CONTACT, state=Call.phone)
async def del_records_del(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(-1001563476682, f"""Пользователь: @{message.from_user.username}
        Номер телефона: {message.contact['phone_number']}
        Требует обратную связь""")
    await bot.send_message(message.from_user.id, "В ближайшее время вам перезвонят.")

@dp.message_handler(commands="contacts")
async def cmd_start(message: types.Message):
    await message.answer(
        "Отвечаем на вопросы ежедневно с 10 до 20 часов по телефону +7 (965) 392-61-69.")

@dp.message_handler(commands="mailing")
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton('Оставили телефон'))
    markup.add(KeyboardButton('Не оставили телефон'))
    await message.answer(
        "Чтобы пустить рассылку по пользователям выберите категорию пользователей введите текст", reply_markup=markup)
    await Mailing.status.set()

@dp.message_handler(state=Mailing.status)
async def cmd_start(message: types.Message, state: FSMContext):
    await state.update_data(status=message.text)
    await message.answer(
        "Чтобы пустить рассылку по пользователям введите текст")
    await Mailing.text.set()

@dp.message_handler(state=Mailing.text)
async def del_records_del(message: types.Message, state: FSMContext):
    mes = message.text
    data = await state.get_data()
    await state.finish()
    await bot.send_message(message.from_user.id, f"Рассылка началась")
    for i in db.get_users():
        if data['status'] == 'Оставили телефон':
            if i[1] == 'Прошёл':
                await bot.send_message(i[0], mes)
        else:
            if i[1] == 'Не прошёл':
                await bot.send_message(i[0], mes)

@dp.message_handler(commands="get_users")
async def cmd_start(message: types.Message):
    mes = ""
    for i in db.get_all_users():
        mes += f"id: {i[0]}, @{i[1]}, {i[2]}, {i[3]}\n"

    await bot.send_message(message.from_user.id, mes)

@dp.message_handler(commands="send_message")
async def cmd_start(message: types.Message):
    await message.answer(
        "Введите id пользователя")
    await Mailing.id.set()

@dp.message_handler(state=Mailing.id)
async def del_records_del(message: types.Message, state: FSMContext):
    mes = message.text
    await bot.send_message(message.from_user.id, "Чтобы отправить сообщению пользователю введите текст")
    await Mailing.text.set()

@dp.message_handler(state=Mailing.text)
async def del_records_del(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data['id'], data['text'])
    await bot.send_message(message.from_user.id, "Сообщение отправлено")
    await state.finish()

@dp.message_handler(commands="send_file")
async def cmd_start(message: types.Message):
    file = message.text[10:]
    print(file)
    await message.answer(
        "Загрузите файл")
    await MailingFile.file.set()

@dp.message_handler(content_types=['photo', 'document'], state=MailingFile.file)
async def del_records_del(message: types.Message, state: FSMContext):
    destination = r"file.pdf"
    await message.document.download(destination_file=destination)
    await bot.send_message(message.from_user.id, "Файл загружен")
    await state.finish()

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)