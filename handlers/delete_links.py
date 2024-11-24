from aiogram.types import Message, CallbackQuery

import keyboards.buttons as kb

from notion_database.notion_database import get_link_by_id, delete_link


async def delete_links_command(message: Message):
    """Prompt user to select a link to delete."""
    await message.answer("❌ Какую ссылку вы хотите удалить:", reply_markup=await kb.delete_info_links_bt())


async def delete_exact_link(callback: CallbackQuery):
    """Delete the selected link."""
    # Extract UUID from callback data
    link_id = callback.data.split('_')[-1]
    # Validate UUID
    import uuid

    try:
        uuid.UUID(link_id)
    except ValueError:
        await callback.answer("❌ Некорректный идентификатор ссылки.")
        return

    # Get link data and delete
    data = await get_link_by_id(link_id)
    if not data:
        await callback.answer("❌ Ссылка не найдена.")
        return

    # Delete link
    result = await delete_link(link_id)
    if result:
        await callback.answer("✅ Ссылка успешно удалена.")
        await callback.message.edit_text("✅ Ссылка удалена.", reply_markup=None)
    else:
        await callback.answer("❌ Не удалось удалить ссылку.")
