#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json
import os


with open('config.json', 'r') as file:
    config = json.load(file)


API_TOKEN = config['api_key']
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_file(message: types.Message):
    filename = 'Предназначение типологий.pdf'
    file_path = os.path.join(os.path.dirname(__file__), filename)
    with open('introduce.txt', 'r', encoding='utf-8') as text:
        await message.answer(text.read())

    msg = await message.answer(f"Начинаю загрузку файла: ⬜⬜⬜")

    # Загрузка и отправка файла
    async def upload_file():
        try:
            with open(file_path, 'rb') as file:
                await bot.send_document(chat_id=message.chat.id, document=file)
        except Exception as e:
            await msg.edit_text(f"Ошибка при отправке файла, повторите комаду /start еще раз ")

    async def update_progress():
        text = "⬜⬜⬜"
        while True:
            if msg.text.count('⬜') < 3:
                break
            next_text = text.replace('⬜', '🟩', 1)
            if next_text != text:
                text = next_text
                await msg.edit_text(f"Начинаю загрузку файла: {text}")
            await asyncio.sleep(1)

    upload_task = asyncio.create_task(upload_file())
    progress_task = asyncio.create_task(update_progress())

    await upload_task
    await msg.edit_text("Загрузка завершена!")
    await message.answer("Хотите прочитать разбор предназначения Майкла Джексона? Жмите /review")
    await progress_task


@dp.message_handler(commands=["review"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    await message.answer('Хочу ознакомить тебя с разбором Майкла Джексона, чтобы у тебя было '
                               'представление сколько информации кроет дата рождения ')

    button1 = types.KeyboardButton(text="Далее")
    keyboard.add(button1)

    await message.answer("Нажми кнопку, чтобы посмотреть разбор", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Далее')
async def send_long_text_with_photo(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton(text="Далеe")
    keyboard.add(button2)

    photo_path = "MJ.jpg"

    with open(photo_path, 'rb') as photo:
        await message.answer_photo(photo)

    with open('michael_jackson.txt', 'r', encoding='utf-8') as text:
        await message.answer(text.read())

    await message.answer("Нажми кнопку, чтобы продолжить", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Далеe')
async def handle_another_button(message: types.Message):

    with open('link.txt', 'r', encoding='utf-8') as text:
        link = text.read()

    keyboard = types.ReplyKeyboardRemove()
    await message.answer(link, reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp)