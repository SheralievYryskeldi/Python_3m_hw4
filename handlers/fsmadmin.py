from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot_instance import dp, bot
from database import bot_db

class FSMADMIN(StatesGroup):
    id = State()
    username = State()
    first_name = State()
    last_name = State()

async def is_admin_func(message: types.Message):
    global ADMIN_ID
    ADMIN_ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Admin, What do u need")

async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        current_state = await state.get_state()
        await state.finish()
        await message.reply("Canceled Successfully")

async def fsm_start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await FSMADMIN.id.set()
        await message.reply("Admin, Send me id please")

async def load_username(message: types.Message,
                        state: FSMContext):
    # if message.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data["username"] = message.text
        # await FSMADMIN.next()
        # await message.reply("Send me username")
        await bot_db.sql_command_insert(state)
        await state.finish()

async def load_first_name(message: types.Message,
                          state: FSMContext):
    # if message.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data["first_name"] = message.text
        # await FSMADMIN.next()
        # await message.reply("Send me user's first name")
        await bot_db.sql_command_insert(state)
        await state.finish()

async def load_last_name(message: types.Message,
                         state: FSMContext):
    # if message.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data["last_name"] = message.text
        # await FSMADMIN.next()
        # await message.reply("Send me user's last_name")
        await bot_db.sql_command_insert(state)
        await state.finish()

async def complete_delete(call: types.CallbackQuery):
    await bot_db.sql_command_delete(call.data.replace("delete ", ""))
    await call.answer(text=f"{call.data.replace('delete ', '')} deleted", show_alert=True)

async def delete_data(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        inserting = await bot_db.sql_casual_select()
        for result in inserting:
            await bot.send_photo(message.from_user.id, result[0],
                                 caption=f'id {result[1]}\n'
                                         f'username {result[2]}',
                                 reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                     f"delete: {result[1]}",
                                     callback_data=f'delete {result[1]}'
                                 )))

def register_handler_fsadmin(dp: Dispatcher):
    dp.register_message_handler(is_admin_func, commands=['admin'], is_chat_admin=True)
    dp.register_message_handler(fsm_start, commands=['id'], state=None)
    dp.register_message_handler(load_username, state=FSMADMIN.username)
    dp.register_message_handler(load_first_name, state=FSMADMIN.first_name)
    dp.register_message_handler(load_last_name, state=FSMADMIN.last_name)
    dp.register_message_handler(cancel_handler, state="*", commands="cancel")
    dp.register_message_handler(cancel_handler, Text(equals="cancel", ignore_case=True), state="*")
    dp.register_callback_query_handler(complete_delete, lambda call: call.data and call.data.startswith('delete '))
    dp.register_message_handler(delete_data, commands=['delete'])
