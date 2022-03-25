import sqlite3
from bot_instance import dp, bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()
    if db:
        print("Database connected successfully")
    db.execute("CREATE TABLE IF NOT EXISTS users"
               "(id TEXT PRIMARY KEY, username TEXT PRIMARY KEY, fist_name TEXT, last_name TEXT)")
    db.commit()

async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", tuple(data.values()))
        db.commit()

async def sql_command_delete(data):
    cursor.execute("DELETE FROM users WHERE id == ?", (data,))
    db.commit()

async def sql_command_select(message):
    for result in cursor.execute("SELECT * FROM users").fetchall():
        await bot.send_message(message.from_user.id, caption=f'id {result[0]}')
        await bot.send_message(message.from_user.id, caption=f'username {result[1]}')
        await bot.send_message(message.from_user.id, caption=f'first_name {result[2]}')
        await bot.send_message(message.from_user.id, caption=f'last_name {result[3]}')

async def sql_casual_select():
    return cursor.execute("SELECT * FROM users").fetchall()