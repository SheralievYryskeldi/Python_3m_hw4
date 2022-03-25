from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from bot_instance import dp, bot
from database import bot_db

async def show_all_users_command(message: types.Message):
    await bot_db.sql_command_insert(message)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(show_all_users_command, commands=['users'])