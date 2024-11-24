import logging

from aiogram.client.session import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
print(f"NOTION_TOKEN: {NOTION_TOKEN}")
print(f"NOTION_DATABASE_ID: {NOTION_DATABASE_ID}")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


async def create_page(data: dict) -> dict:
    """Создаёт страницу в Notion."""
    create_url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": data
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(create_url, headers=headers, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_data = await response.json()
                raise Exception(f"Failed to create page: {response.status}, {error_data}")


async def get_all_links() -> list:
    """Получает все ссылки из базы данных Notion."""
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"

    query_payload = {
        "filter": {
            "property": "URL",
            "url": {
                "is_not_empty": True
            }
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=query_payload) as response:
            if response.status == 200:
                data = await response.json()
                links = []
                for result in data['results']:
                    # Получаем название, ID и URL
                    title = result['properties']['Title']["rich_text"][0]["text"]["content"]  # Предполагается, что название находится в свойстве 'Name'
                    link_id = result['id']  # ID записи
                    links.append({'title': title, 'id': link_id})  # Сохраняем в виде словаря
                return links
            else:
                error_data = await response.json()
                raise Exception(f"Failed to get links: {response.status}, {error_data}")

async def get_link_by_id(link_id: str) -> dict:
    """Получает ссылку по ID из базы данных Notion."""
    url = f"https://api.notion.com/v1/pages/{link_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                # Получаем все необходимые поля
                result = {
                    'title': data['properties']['Title']["rich_text"][0]["text"]["content"],
                    'url': data['properties']['URL']["title"][0]["text"]["content"],
                    'category': data['properties']['Category']["rich_text"][0]["text"]["content"],
                    'source': data['properties']['Source']["rich_text"][0]["text"]["content"],
                    'priority': data['properties']['Priority']["number"],
                    'timestamp': data['properties']["Timestamp"]["date"]["start"],  # Получаем только дату
                    'id': link_id
                }
                return result
            else:
                error_data = await response.json()
                raise Exception(f"Failed to get link by ID: {response.status}, {error_data}")


async def delete_link(link_id: str) -> dict:
    """Удаляет страницу в Notion по ID."""
    delete_url = f"https://api.notion.com/v1/pages/{link_id}"  # Изменено с /links/ на /pages/
    payload = {"archived": True}

    async with aiohttp.ClientSession() as session:
        async with session.patch(delete_url, json=payload, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_data = await response.json()
                logging.error(f"Request URL: {delete_url}")
                logging.error(f"Request Payload: {payload}")
                logging.error(f"Response: {response.status}, {error_data}")
                raise Exception(f"Failed to delete link: {response.status}, {error_data}")
