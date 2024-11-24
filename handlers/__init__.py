from aiogram import Router, F
from aiogram.filters import CommandStart

from handlers.commands import (start_command_handler, process_back_callback, process_menu_callback)

from handlers.add_links import add_link_command, process_url, process_title, process_priority, process_category
from handlers.delete_links import delete_exact_link, delete_links_command
from handlers.get_links import get_all_links_command, link


from states.link_states import LinkStates as st



def setup() -> Router:
    router = Router()

    # Регистрация команд
    router.message.register(start_command_handler, CommandStart())
    router.message.register(add_link_command, F.text == "➕ Добавить ссылку")
    router.message.register(get_all_links_command, F.text == "📜 Получить ссылки")
    router.message.register(delete_links_command, F.text == "❌ Удалить ссылку")
    # Регистрация состояний
    router.message.register(process_url, st.waiting_for_url)
    router.message.register(process_title, st.waiting_for_title)
    router.message.register(process_category, st.waiting_for_category)
    router.message.register(process_priority, st.waiting_for_priority)

    # Регистрация callback query handlers
    router.callback_query.register(link, F.data.startswith("link_"))
    router.callback_query.register(delete_exact_link, F.data.startswith("del_link_"))
    router.callback_query.register(process_back_callback, lambda c: c.data == "go_back")
    router.callback_query.register(process_menu_callback, lambda c: c.data == "to_main")
    router.callback_query.register(delete_exact_link, lambda c: c.data.startswith("delete_exact_link_"))

    return router
