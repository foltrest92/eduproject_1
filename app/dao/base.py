from uuid import UUID

from sqlalchemy import UpdateBase, delete, insert, select, update

from app.database import async_session_maker
from app.exceptions import NoFoundException

class BaseDAO:
    model = None
    uid = None

    @classmethod
    async def _select(cls, query: list[UpdateBase] | UpdateBase):
        async with async_session_maker() as session:
            if isinstance(query, list):
                result = [await session.execute(q) for q in query]
            else:
                result = await session.execute(query)
            return result
    
    @classmethod
    async def _update_base(cls, query: list[UpdateBase] | UpdateBase):
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
        mapped = await cls._select(query).mappings().one_or_none()
        if mapped:
            return mapped
        raise NoFoundException()

    @classmethod
    async def select_one_or_none(cls, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        result = await cls._select(query)
        return result.mappings().one_or_none()


    @classmethod
    async def select(cls, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        result = await cls._select(query)
        return result.mappings().all()

    @classmethod
    async def insert(cls, **data):
        query = insert(cls.model).values(**data).returning(cls.model)
        result = await cls._update_base(query)
        return result.scalar_one()
    
    @classmethod
    async def update(cls, model_id: int, **data):
        query = update(cls.model).where(cls.uid == model_id).values(**data).returning(cls.model)
        result = await cls._update_base(query)
        return result.scalar_one()

    @classmethod
    async def delete(cls, model_id: int) -> bool:
        query = delete(cls.model).where(cls.uid == model_id)
        result = await cls._update_base(query)
        return bool(result.rowcount)