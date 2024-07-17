from uuid import UUID
from sqlalchemy import delete, insert, select, update
from app.database import async_session_maker
from app.exceptions import NoFoundException


class BaseDAO:
    model = None
    uid = None

    @classmethod
    async def find_by_id(cls, model_id: int | UUID):
        async with async_session_maker() as session:
            filter = {cls.uid.name:model_id}
            query = select(cls.model.__table__.columns).filter_by(**filter)
            result = await session.execute(query)
            mapped = result.mappings().one_or_none()
            if mapped:
                return mapped
            raise NoFoundException()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()



    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
    
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()
    
    @classmethod
    async def update(cls, model_id: int, **data):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.uid == model_id).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def delete(cls, model_id: int) -> bool:
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.uid == model_id)
            result = await session.execute(query)
            await session.commit()
            return bool(result.rowcount)