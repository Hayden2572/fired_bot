from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btn = [
        [InlineKeyboardButton(text="Открыть ВЕБ", url="https://127.0.0.1:8000")],
        [InlineKeyboardButton(text="Удалить сотрудника", callback_data='kick_user')]
    ]



channel_list = [
    [InlineKeyboardButton(text='Тут пока нет каналов', url='vk.com')],
    [InlineKeyboardButton(text='Меню', callback_data='back')]

]
keyboard = InlineKeyboardMarkup(inline_keyboard=btn)
channel_kb = InlineKeyboardMarkup(inline_keyboard=channel_list)
