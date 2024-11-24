from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from notion_database.notion_database import get_all_links, get_link_by_id, delete_link


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='➕ Добавить ссылку')],
    [KeyboardButton(text='📜 Получить ссылки')],
    [KeyboardButton(text='❌ Удалить ссылку')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню...')

async def go_back_bt() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="go_back")]
        ]
    )
    return keyboard

# GET LINKS BT
async def all_links_bt():
    all_links = await get_all_links()
    keyboard = InlineKeyboardBuilder()

    for link in all_links:
        keyboard.add(InlineKeyboardButton(text=link['title'], callback_data=f"link_{link['id']}"))

    keyboard.add(InlineKeyboardButton(text='🏠 На главную', callback_data='to_main'))

    return keyboard.adjust(2).as_markup()


async def exact_link_bt(link_id):
    exact_link = await get_link_by_id(link_id)
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text=exact_link['title'],
        callback_data=f'exact_link_{link_id}'
    ))
    InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⬅️ Назад к списку', callback_data='go_back')],
        [InlineKeyboardButton(text='🏠 На главную', callback_data='to_main')]
    ])
    return keyboard.adjust(2).as_markup()

# DELETE BT
async def delete_info_links_bt():
    del_info_links = await get_all_links()
    keyboard = InlineKeyboardBuilder()

    for link in del_info_links:
        keyboard.add(InlineKeyboardButton(text=link['title'], callback_data=f"del_link_{link['id']}"))

    keyboard.add(InlineKeyboardButton(text='🏠 На главную', callback_data='to_main'))

    return keyboard.adjust(2).as_markup()






