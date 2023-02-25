import logging
import time
import requests
import random

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import TOKEN
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton("/help")
b2 = KeyboardButton("/description")
b3 = KeyboardButton("/location")
b4 = KeyboardButton("/😝")
b5 = KeyboardButton("/💻")
kb.add(b1).insert(b2).add(b3).insert(b4).add(b5)

manual = """
<em>Вот что я умею</em> 
<b>1.</b>  <em> /start - Запуск БОТА </em>
<b>2.</b>  <em> /description - Описание обота </em> 
<b>3.</b>  <em> /location - Место нахождения </em>
<b>4.</b>  <em> /😝 - Стикер </em>
<b>5.</b>  <em> /parser - Возможно появится </em>
<b>6.</b>  <em> /💻 - Примерные фото корпусов </em>
"""


URL = "https://torg-pc.ru/catalog/igrovye-kompyutery/"

def parser(url):

    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    game_pc = soup.find_all("div", class_="item-title")
    return [c.text for c in game_pc]


list_of_pc = parser(URL)
random.shuffle(list_of_pc)

async def on_startup(_):
    print("Бот запущен")


@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=manual,
                           parse_mode="HTML")
    await message.delete()


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f"{user_id=} {user_full_name=} {time.asctime()}")
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"<em>Добро пожаловать</em>, <b>{user_full_name} !</b>",
                           parse_mode="HTML",
                           reply_markup=kb)


@dp.message_handler(commands=["description"])
async def description_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"<b>Этот бот умеет.... Да не фига он не умеет...</b>",
                           parse_mode="HTML")
    await message.delete()


@dp.message_handler(commands="💻")
async def send_image(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo="https://torg-pc.ru/upload/iblock/4c0/wd5c5n2ph462143kuk94ozhnam80aexg/MPGVELOX100R.webp")
    await bot.send_photo(chat_id=message.from_user.id,
                         photo="https://hyperpc.ru/images/product/cyber/gallery/black/"
                               "hyperpc-cyber-black-build-photo-01.jpg")
    await bot.send_photo(chat_id=message.from_user.id,
                         photo="https://torg-pc.ru/upload/iblock/f5b/7a1705j4idbq7mn47bf0qgmb5r6vy2sa/main.png")
    await bot.send_photo(chat_id=message.from_user.id,
                         photo="https://digital-discount.ru/wp-content/"
                               "uploads/4/a/7/4a70fcbf7371e982683c3b9e11123dcc.jpeg")
    await bot.send_photo(chat_id=message.from_user.id,
                         photo="https://hyperpc.ru/images/product/dynamic/product_gallery/update/"
                               "hyperpc-dynamic-update-1-build-photo-01.jpg")
    await bot.send_photo(chat_id=message.from_user.id,
                         photo="https://torg-pc.ru/upload/resize_cache/iblock/1ef/6984zbivx7swjze8bwr8apr30qp322h4/"
                               "750_650_140cd750bba9870f18aada2478b24840a/1STPLAYERFIREBASEXP-EBLack1.webp")
    await message.delete()


@dp.message_handler(commands=["location"])
async def send_point(message: types.Message):
    await bot.send_location(chat_id=message.from_user.id,
                            latitude=56.3448,
                            longitude=37.5204)
    await message.delete()


@dp.message_handler(commands=["😝"])
async def send_message(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEH21Zj9i95Fyv2JPQtEjiriPUrbe5DngACbgADpsrIDGq"
                                                         "ftCjcFYikLgQ")
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAIFYGP5KbPYt2UZlW2XPQr0WaWlMX40AAJsAAMNttIZ9B0"
                                                         "1C5GR3kQuBA")
    await message.delete()


@dp.message_handler(content_types=['parser'])
async def send_parser(message: types.Message):
    if message.text.lower() in "parser":
        await bot.send_message(message.from_user.id, list_of_pc[0])
        del list_of_pc[0]
    else:
        await bot.send_message(message.from_user.id, "Не привильно написано")


@dp.message_handler(content_types=["sticker"])
async def send_sticker_id(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAIEAAFj9nTiv8VUbzQOg9GrimK-ty808gACzBgAAntYUEmw"
                                                         "TZrmztcawi4E")
    await message.answer(message.sticker.file_id)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
    await bot.send_message(chat_id=message.from_user.id,
                           text="И что это?😡")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)