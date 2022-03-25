from aiogram import executor
from bot_instance import dp
from handlers import fsmadmin
from database import bot_db

async def on_startup(_):
    bot_db.sql_create()

fsmadmin.register_handler_fsadmin(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup())