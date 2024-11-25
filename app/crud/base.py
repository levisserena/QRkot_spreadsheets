from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(self, object_id: int, session: AsyncSession):
        """Возвращает объект из таблицы по id."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == object_id)
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        """Возвращает все объекты из таблицы."""
        db_obj = await session.execute(select(self.model))
        return db_obj.scalars().all()

    async def get_by_attribute(
            self,
            attr_name: str,
            attr_value: str,
            session: AsyncSession,
    ):
        """Возвращает объект из таблицы по значению атрибута."""
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()

    async def create(
        self, object_in, session: AsyncSession, user: Optional[User] = None
    ):
        """Создаёт объект в таблице."""
        object_in_data = object_in.dict()
        if user is not None:
            object_in_data['user_id'] = user.id
        db_object = self.model(**object_in_data)
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def update(self, db_object, object_in, session: AsyncSession):
        """Обновляет объект в таблице."""
        object_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)
        for field in object_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def remove(self, db_object, session: AsyncSession):
        """Удаляет объект из таблицы."""
        await session.delete(db_object)
        await session.commit()
        return db_object
