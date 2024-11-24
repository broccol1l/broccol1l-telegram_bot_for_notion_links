from datetime import datetime, timezone


from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.validators import get_source_from_url

import keyboards.buttons as kb
import database.requests as rq
from states.link_states import LinkStates as st

from notion_database.notion_database import create_page, get_link_by_id, delete_link
async def start_command_handler(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f"С возвращением, {message.from_user.full_name}! Чем могу помочь?😁", reply_markup=kb.main)


async def process_back_callback(callback_query: CallbackQuery):
    """Handle back navigation."""
    await callback_query.message.edit_text(
        "Вот все доступные ссылки:",
        reply_markup=await kb.all_links_bt()
    )
    await callback_query.answer()


async def process_menu_callback(callback_query: CallbackQuery):
    """Display main menu options."""
    await callback_query.message.answer(
        "Чем могу помочь?",
        reply_markup=kb.main
    )
    await callback_query.answer()

