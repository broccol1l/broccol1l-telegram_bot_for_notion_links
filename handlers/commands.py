from aiogram.types import Message, CallbackQuery

import keyboards.buttons as kb
import database.requests as rq

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

