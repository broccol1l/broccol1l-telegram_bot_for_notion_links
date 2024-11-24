from database.engine import async_session
from models.models import User, Link
from sqlalchemy import select, update, delete


async def set_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def add_link(tg_id: int, url: str, title: str, category: str, source: str, priority: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        link = Link(url=url, title=title, category=category, source=source, priority=priority, user=user)
        session.add(link)
        await session.commit()

async def delete_link(link_id: int):
    async with async_session() as session:
        await session.execute(delete(Link).where(Link.id == link_id))
        await session.commit()

async def update_link(link_id: int, url: str, title: str, category: str, source: str, priority: int):
    async with async_session() as session:
        await session.execute(
            update(Link)
            .where(Link.id == link_id)
            .values(url=url, title=title, category=category, source=source, priority=priority)
        )
        await session.commit()

async def get_link(link_id: int):
    async with async_session() as session:
        return await session.scalar(select(Link).where(Link.id == link_id))


async def get_all_links():
    async with async_session() as session:
        return await session.scalars(select(Link))
