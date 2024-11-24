from datetime import datetime, timezone


from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.validators import get_source_from_url, is_valid_url

import keyboards.buttons as kb
import database.requests as rq
from states.link_states import LinkStates as st

from notion_database.notion_database import create_page



async def add_link_command(message: Message, state: FSMContext):
    """Prompt user to send a URL for saving."""
    await message.answer("🔗 Отправьте ссылку для сохранения")
    await state.set_state(st.waiting_for_url)


# Process the URL
async def process_url(message: Message, state: FSMContext):
    """Process and save URL data."""
    url = message.text
    re_url = await is_valid_url(url)

    if re_url:
        await message.answer(f"✅ Ссылка '{url}' успешно сохранена!")
        await state.update_data(url=url)
        await message.answer("📝 Теперь отправьте заголовок для ссылки.")
        await state.set_state(st.waiting_for_title)
    else:
        await message.answer("❌ Неверная ссылка. Пожалуйста, отправьте действительную ссылку.")
        await state.set_state(st.waiting_for_url)


# Process the Title
async def process_title(message: Message, state: FSMContext):
    """Process and save title data."""
    title = message.text.capitalize()
    await state.update_data(title=title)
    await message.answer("📂 Напишите категорию для ссылки.")
    await state.set_state(st.waiting_for_category)


# Process the Category
async def process_category(message: Message, state: FSMContext):
    """Process and save category data."""
    category = message.text.capitalize()
    await state.update_data(category=category)

    # Переход к следующему шагу без запроса приоритета
    url = (await state.get_data()).get('url')  # Получаем URL из состояния
    source = await get_source_from_url(url)

    # Сохраняем автоматически извлеченный источник в состояние
    await state.update_data(source=source)

    await message.answer(f"🔍 Источник автоматически установлен: {source}\n\n"
                         "⭐ Теперь отправьте приоритет для ссылки:\n"
                         "1️⃣ - Самая высокая приоритетность\n"
                         "2️⃣ - Средняя приоритетность\n"
                         "3️⃣ - Самая низкая приоритетность\n"
                         "Пожалуйста, введите число от 1 до 3."
                         )

    # Переход к шагу приоритета
    await state.set_state(st.waiting_for_priority)

async def process_priority(message: Message, state: FSMContext):
    priority = int(message.text)

    if priority <= 3 and priority >= 1:
        data = await state.get_data()

        url = data.get('url')
        title = data.get('title')
        category = data.get('category')
        source = data.get('source')
        tg_id = message.from_user.id

        timestamp = datetime.now(timezone.utc).isoformat()

        dt = datetime.fromisoformat(timestamp)

        formatted_timestamp = dt.strftime("%d-%m-%Y %H:%M:%S")

        notion_data = {
            "URL": {"title": [{"text": {"content": url}}]},
            "Title": {"rich_text": [{"text": {"content": title}}]},
            "Category": {"rich_text": [{"text": {"content": category}}]},
            "Source": {"rich_text": [{"text": {"content": source}}]},
            "Priority": {"number": priority},
            "Timestamp": {"date": {"start": timestamp}},
            "Telegram_user_id": {"number": tg_id}
        }
        await create_page(notion_data)

        await rq.add_link(
            tg_id=message.from_user.id,
            url=data['url'],
            title=data['title'],
            category=data['category'],
            source=data['source'],
            priority=priority
        )

        await message.answer("✅ Ссылка успешно добавлена!\n\n"
                             f"🔗 *URL:* {data['url']}\n"
                             f"📝 *Заголовок:* {data['title']}\n"
                             f"📂 *Категория:* {data['category']}\n"
                             f"🔍 *Источник:* {data['source']}\n"
                             f"⭐ *Приоритет:* {priority}\n"
                             f"📅 *Дата добавления:* {formatted_timestamp}",
                             reply_markup=kb.main
                             )
        await state.clear()
    else:
        await message.answer("❌Пожалуйста, введите число от 1 до 3.")