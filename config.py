import time
import logging
import telebot
from telebot import types
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

TOKEN = "5808982110:AAGjlpy6UMnO6279ynxtiCfH22pbrQ_Dh1w"

MSG = "За кодинг, {} !"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

# bot = telebot.TeleBot(TOKEN)


manual = """
<em>Вот что я умею</em> 
<b>1.</b>  <em> /start - Запуск БОТА </em>
<b>2.</b>  <em> /location - Место нахождения </em>
<b>3.</b>  <em> /give - Стикер </em>
<b>4.</b>  <em> /parser - возможно появится </em>
<b>5.</b>  <em> /картинки - примерные фото корпусов </em>
"""


async def on_startup(_):
    print("Бот запущен")


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f"{user_id=} {user_full_name=} {time.asctime()}")

    await message.answer(f"<em>Привет</em>, <b>{user_full_name}</b>", parse_mode="HTML")

    for i in range(5):
        time.sleep(10)
        await bot.send_message(user_id, MSG.format(user_name))


@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    await bot.send_message(chat_id=message.from_user.id,
                           text=manual, parse_mode="HTML")
    await message.delete()
    logging.info(f"{user_id}: {user_full_name}: {time.asctime()}")


@dp.message_handler(commands=["give"])
async def send_message(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEH21Zj9i95Fyv2JPQtEjiriPUrbe5DngACbgADpsrIDGq"
                                                         "ftCjcFYikLgQ")
    await message.delete()
    logging.info(f"{time.asctime()}")


@dp.message_handler(content_types=["sticker"])
async def send_sticker_id(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAIEAAFj9nTiv8VUbzQOg9GrimK-ty808gACzBgAAntYUEmw"
                                                         "TZrmztcawi4E")
    await message.answer(message.sticker.file_id)


@dp.message_handler(commands=["картинки"])
async def send_image(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,
                         photo="https://digital-discount.ru/wp-content/"
                               "uploads/5/7/9/57961b6bdec3f701f79ac55619ba5af0.jpeg")
    await bot.send_photo(chat_id=message.chat.id,
                         photo="https://hyperpc.ru/images/product/cyber/gallery/black/"
                               "hyperpc-cyber-black-build-photo-01.jpg")
    await bot.send_photo(chat_id=message.chat.id,
                         photo="https://ae01.alicdn.com/kf/UTB8ECsnCJoSdeJk43Owq6ya4XXaH.jpg")
    await message.delete()


@dp.message_handler(commands=["location"])
async def send_point(message: types.Message):
    await bot.send_location(chat_id=message.from_user.id,
                            latitude=56.3448,
                            longitude=37.5204)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
    await bot.send_message(chat_id=message.from_user.id,
                           text="И что это?😡")



# @dp.message_handler(commands=["parser"])
# async def parser_site(message: types.Message):
#     text = message.text.split()[1]
#     await bot.send_message(chat_id=message.from_user.id)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)