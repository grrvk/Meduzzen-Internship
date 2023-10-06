from abc import ABC, abstractmethod

from fastapi import HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import SessionLocal


class AbstractRepository(ABC):
    @abstractmethod
    async def create_one(self, data):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_one_by(self, data):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def create_one(self, data: dict) -> int:
        async with SessionLocal() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def update_one(self, id: int, data: dict):
        async with SessionLocal() as session:
            stmt = update(self.model).filter_by(id=id).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_all(self):
        async with SessionLocal() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res

    async def get_one_by(self, **filter_by):
        async with SessionLocal() as session:
            try:
                stmt = select(self.model).filter_by(**dict(filter_by))
                res = await session.execute(stmt)
                res = res.scalar_one().to_read_model()
                return res
            except SQLAlchemyError as e:
                return None

    async def delete_one(self, id: int):
        async with SessionLocal() as session:
            stmt = delete(self.model).filter_by(id=id)
            res = await session.execute(stmt)
            await session.commit()
            return True
