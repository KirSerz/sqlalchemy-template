from typing import Type, TypeVar, Generic, Optional, Any, Sequence

from sqlalchemy import select, func, Row, RowMapping
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Base repository providing common CRUD operations for async sessions.
    """

    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(
        self,
        pk: int = None,
        filters: Optional[list] = None,
        joins: Optional[list] = None,
        left_joins: Optional[list[tuple[Any, Any]]] = None,
        order_by=None,
        options: Optional[list] = None,
    ) -> Optional[T]:
        """
        Retrieve a single record by its ID or using optional filters, joins, ordering and loader options.
        If 'id' is provided, it will be added as a filter.
        """
        filters = filters or []
        joins = joins or []
        left_joins = left_joins or []
        options = options or []

        if pk is not None:
            filters.append(self.model.id == pk)

        query = select(self.model).where(*filters)

        for join_item in joins:
            query = query.join(join_item)

        for left_join_item in left_joins:
            target, condition = left_join_item
            query = query.outerjoin(target, condition)

        if order_by is not None:
            query = query.order_by(order_by)

        for opt in options:
            query = query.options(opt)

        result = await self.session.execute(query.with_for_update())
        return result.scalar_one_or_none()

    async def get_all(
        self,
        filters: Optional[list] = None,
        joins: Optional[list] = None,
        left_joins: Optional[list[tuple[Any, Any]]] = None,
        limit: int = 10,
        offset: int = 0,
        order_by=None,
        options: Optional[list] = None,
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        """
        Retrieve all records with optional filters, joins, pagination, ordering and loader options.
        """
        filters = filters or []
        joins = joins or []
        left_joins = left_joins or []
        options = options or []

        query = select(self.model).where(*filters)

        for join_item in joins:
            query = query.join(join_item)

        for left_join_item in left_joins:
            target, condition = left_join_item
            query = query.outerjoin(target, condition)

        if order_by is not None:
            if isinstance(order_by, list) or isinstance(order_by, tuple):
                query = query.order_by(*order_by)
            else:
                query = query.order_by(order_by)

        query = query.limit(limit).offset(offset)

        for opt in options:
            query = query.options(opt)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, instance: T) -> T:
        """
        Create a new record.
        """
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def bulk_create(self, instances: list[T]) -> None:
        self.session.add_all(instances)
        await self.session.commit()

    async def update(self, pk: int, **kwargs) -> T:
        """
        Update a record by ID.
        """
        obj = await self.get(pk)
        if not obj:
            raise NoResultFound(f"{self.model.__name__} with id {pk} not found")

        for key, value in kwargs.items():
            setattr(obj, key, value)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, pk: int) -> Optional[T]:
        """
        Delete a record by ID.
        """
        obj = await self.get(pk)
        if not obj:
            raise NoResultFound(f"{self.model.__name__} with id {pk} not found")

        await self.session.delete(obj)
        await self.session.commit()
        return obj

    async def count(
        self,
        filters: Optional[list] = None,
        joins: Optional[list] = None,
        left_joins: Optional[list[tuple[Any, Any]]] = None,
    ) -> int:
        """
        Count the number of records with optional filters and joins.
        """
        filters = filters or []
        joins = joins or []
        left_joins = left_joins or []

        query = select(func.count()).select_from(self.model).where(*filters)

        for join_item in joins:
            query = query.join(join_item)

        for left_join_item in left_joins:
            target, condition = left_join_item
            query = query.outerjoin(target, condition)

        result = await self.session.execute(query)
        return result.scalar()
