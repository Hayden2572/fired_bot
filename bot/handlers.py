from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from keyboards import keyboard, channel_kb
from config import bot, BOT_TOKEN
from aiogram.fsm.context import FSMContext
import sqlite3
from aiogram.fsm.state import StatesGroup, State

from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

channel_list = []
[InlineKeyboardButton(text='Тут пока нет каналов', url='vk.com')]

cursor.execute('SELECT channel FROM users ')
id_count = cursor.fetchall()
for idd in id_count:
    channel_list.append(idd[0])
connection.commit()



router = Router()
need_to_kick = ''

class Form(StatesGroup):
    waiting_for_message = State()
@router.callback_query(lambda c: c.data == 'kick_user')
async def start_message_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите юзернейм сотрудника")
    await state.set_state(Form.waiting_for_message)

@router.message(Form.waiting_for_message)
async def handle_user_message(message: Message, state: FSMContext):
    global need_to_kick
    info_messages = []
    for channel_id in channel_list:
        chat = await bot.get_chat(channel_id)
        if chat.title == None:
            continue
        else:
            info_messages.append([InlineKeyboardButton(text=chat.title, callback_data=f'action:{chat.id}')])
    channel_kb = InlineKeyboardMarkup(inline_keyboard=info_messages)
    if message.text[0] == '@':    
        need_to_kick = message.text
        await message.answer("выберите канал:", reply_markup=channel_kb)
        await state.clear()
    else:
        await message.answer("формат хуйня")

@router.callback_query(lambda c: c.data and c.data.startswith("action:"))
async def handle_callback(query: CallbackQuery):
    global need_to_kick
    async with TelegramClient('session.session', api_id=27475062, api_hash='e5f5b0942cf516ddc88ba9f234d1d3a8') as client:
        user = await client(GetFullUserRequest(need_to_kick[1:]))
    kicked = user.full_user.id
    action, value = query.data.split(":")
    await bot.ban_chat_member(chat_id=value, user_id=kicked)
    await bot.send_message(chat_id=value, text = f"Пользователь {need_to_kick} был забанен нахуй")

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Нажмите на кнопку:", reply_markup=keyboard)


chats = set()

@router.message(Command('save'))
async def track_chat_ids(message: Message):
    save_id = message.chat.id
    cursor.execute('SELECT id FROM users ')
    id_count = cursor.fetchone()
    for idd in id_count:
        res = idd
    res += 1
    connection.commit()
    cursor.execute(f"INSERT INTO users (id, channel) SELECT {res}, '{save_id}' WHERE NOT EXISTS (SELECT 1 FROM users WHERE channel = '{save_id}');")
    connection.commit()
    await message.answer("Ваш чат добавлен в список.")

@router.message(Command('show'))
async def track_chat_ids(message: Message):
    await message.answer("Список моих чатов:")
    cursor.execute('SELECT * FROM users ')
    id_count = cursor.fetchall()
    for idd in id_count:
        await message.answer(f'{idd[0]} - {idd[1]}')

@router.callback_query(lambda c: c.data == 'open_channels')
async def process_callback_button1(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберите каналы из которых нужно удалить', reply_markup=channel_kb)




@router.callback_query(lambda c: c.data == 'back')
async def back_to_menu(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберите действие:', reply_markup=keyboard)