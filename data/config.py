import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv('BOT_TOKEN')
DATABASE_URL: str = os.getenv('DATABASE_URL')
NOTION_TOKEN: str = os.getenv('NOTION_TOKEN')
NOTION_DATABASE_ID: str = os.getenv('NOTION_DATABASE_ID')


