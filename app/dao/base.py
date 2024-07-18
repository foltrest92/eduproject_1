from uuid import UUID

from sqlalchemy import UpdateBase, delete, insert, select, update

from app.database import async_session_maker
from app.exceptions import NoFoundException

class BaseDAO:
    model = None
    uid = None

    @classmethod
    async def __select(cls, query: list[UpdateBase] | UpdateBase):
        async with async_session_maker() as session:
            if isinstance(query, list):
                result = [await session.execute(q) for q in query]
            else:
                result = await session.execute(query)
            return result
    
    @classmethod
    async def __update_base(cls, query: list[UpdateBase] | UpdateBase):
        async with async_session_maker() as session:
            if isinstance(query, list):
                result = [await session.execute(q) for q in query]
            else:
                result = await session.execute(query)
            await session.commit()
            return result

    @classmethod
    async def find_by_id(cls, model_id: int | UUID):
        query = select(cls.model.__table__.columns).filter_by(**filter)
        mapped = await cls.__select(query).mappings().one_or_none()
        if mapped:
            return mapped
        raise NoFoundException()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        return await cls.__select(query).mappings().one_or_none()


    @classmethod
    async def select(cls, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        return await cls.__select(query).mappings().all()

    @classmethod
    async def insert(cls, **data):
        query = insert(cls.model).values(**data).returning(cls.model)
        return await cls.__update_base(query).scalar_one()
    
    @classmethod
    async def update(cls, model_id: int, **data):
        query = update(cls.model).where(cls.uid == model_id).values(**data).returning(cls.model)
        return await cls.__update_base(query).scalar_one()

    @classmethod
    async def delete(cls, model_id: int) -> bool:
        query = delete(cls.model).where(cls.uid == model_id)
        return bool(await cls.__update_base(query).rowcount)