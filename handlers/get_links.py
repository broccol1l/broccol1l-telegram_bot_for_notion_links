from aiogram.types import Message, CallbackQuery

import keyboards.buttons as kb

from notion_database.notion_database import get_link_by_id


async def get_all_links_command(message: Message):
    """Show all available links."""
    await message.answer("Вот все доступные ссылки:", reply_markup=await kb.all_links_bt())


async def link(callback: CallbackQuery):
    """Show details of a specific link."""
    link_id = callback.data.split('_')[1]
    data = await get_link_by_id(link_id)

    # Display the link details
    await callback.message.edit_text(
        f"🔗 *URL:* {data['url']}\n"
        f"📝 *Заголовок:* {data['title']}\n"
        f"📂 *Категория:* {data['category']}\n"
        f"🔍 *Источник:* {data['source']}\n"
        f"⭐ *Приоритет:* {data['priority']}\n"
        f"📅 *Дата добавления:* {data['timestamp']}",
        reply_markup=await kb.go_back_bt()
    )
