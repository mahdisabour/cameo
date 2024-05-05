from datetime import datetime
from typing import (Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar,
                    Union)

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.dml import Delete, Insert, Update
from sqlalchemy.sql.expression import delete, select
from sqlalchemy.sql.selectable import Select
from sqlalchemy import func


from app.db.base_class import Base
from app.util.exceptions import CustomDatabaseError
from app.util.tuple_convertor import tuple_first_item

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


DEFAULT_DB_QUERY_LIMIT = 100
INTERNAL_SERVER_ERROR_TEXT = "internal server error"


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, db: Session, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.db = db
        self.model = model

    async def get(self, obj_id: Any) -> Optional[ModelType]:
        try:
            db_obj: Optional[Tuple[ModelType, Any]] = (
                await self.db.execute(
                    select(self.model).where(self.model.id == obj_id),
                )
            ).first()
        except Exception:
            raise Exception(INTERNAL_SERVER_ERROR_TEXT)
        if db_obj is not None:
            return db_obj[0]
        return None

    async def create(
        self,
        *,
        obj_in: CreateSchemaType,
        autocommit: bool = True,
    ) -> ModelType:
        obj_in_data = jsonable_encoder(
            obj_in,
            custom_encoder={datetime: lambda obj: obj}
        )
        db_obj: ModelType = self.model(**obj_in_data)
        self.db.add(db_obj)
        if autocommit:
            try:
                await self.db.commit()
                await self.db.refresh(db_obj)
            except IntegrityError as exc:
                await self.db.rollback()
                raise CustomDatabaseError(str(exc.orig))
            except Exception:
                raise Exception("internal server error")
        return db_obj
    
    def sync_create(
        self,
        *,
        obj_in: CreateSchemaType,
        autocommit: bool = True,
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        self.db.add(db_obj)
        if autocommit:
            try:
                self.db.commit()
                self.db.refresh(db_obj)
            except IntegrityError as exc:
                self.db.rollback()
                raise CustomDatabaseError(str(exc.orig))
            except Exception:
                raise Exception("internal server error")
        return db_obj


    async def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        autocommit: bool = True,
        exclude: list[str] = [],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj, exclude=exclude)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data.get(field))
        if autocommit:
            try:
                await self.db.commit()
                await self.db.refresh(db_obj)
            except IntegrityError as exc:
                await self.db.rollback()
                raise CustomDatabaseError(str(exc.orig))
            except Exception:
                raise Exception("internal server error")
        return db_obj

    async def update_by_clause(
        self,
        clause: Update,
        autocommit: bool = True,
    ) -> int:
        new_object = await self.db.execute(clause)
        if autocommit:
            try:
                await self.db.commit()
            except IntegrityError as exc:
                await self.db.rollback()
                raise CustomDatabaseError(str(exc.orig))
            except Exception:
                raise Exception("internal server error")

        count: int = new_object.rowcount
        return count

    async def create_by_clause(
        self,
        clause: Insert,
        autocommit: bool = True,
    ) -> ModelType:
        try:
            insert_result: ModelType = await self.db.execute(clause)
            if autocommit:
                await self.db.commit()
        except IntegrityError as exc:
            await self.db.rollback()
            raise CustomDatabaseError(str(exc.orig))
        except Exception:
            raise Exception("internal server error")

        return insert_result

    async def remove_by_clause(
        self,
        clause: Delete,
        autocommit: bool = True,
    ) -> int:
        try:
            remove_result = await self.db.execute(clause)
            if autocommit:
                await self.db.commit()
        except Exception:
            raise Exception("internal server error")

        count: int = remove_result.rowcount
        return count

    async def remove(
        self,
        *,
        obj_id: str,
        autocommit: bool = True,
    ) -> int:
        try:
            remove_result = await self.db.execute(
                delete(self.model).where(self.model.id == obj_id),
            )
            if autocommit:
                await self.db.commit()
        except Exception:
            raise Exception("internal server error")

        count: int = remove_result.rowcount
        return count

    async def filter_by_clause(
        self,
        clause: Select,
        skip: int = 0,
        limit: int = DEFAULT_DB_QUERY_LIMIT,
    ) -> List[ModelType]:
        try:
            list_obj: ChunkedIteratorResult[
                Tuple[ModelType, Any]
            ] = await self.db.execute(
                clause.limit(limit).offset(skip),
            )
        except Exception:
            raise Exception("internal server error")

        return list(
            map(tuple_first_item, list_obj),
        )
    
    def sync_filter_by_clause(
        self,
        clause: Select,
        skip: int = 0,
        limit: int = DEFAULT_DB_QUERY_LIMIT,
    ) -> List[ModelType]:
        try:
            list_obj: ChunkedIteratorResult[
                Tuple[ModelType, Any]
            ] = self.db.execute(
                clause.limit(limit).offset(skip),
            )
        except Exception:
            raise Exception("internal server error")

        return list(
            map(tuple_first_item, list_obj),
        )
    
    async def filter_by_clause_with_total(
        self,
        clause: Select,
        skip: int = 0,
        limit: int = DEFAULT_DB_QUERY_LIMIT,
    ) -> Tuple[List[ModelType], int]:
        try:
            # Execute query to get items within limit and skip
            list_obj: ChunkedIteratorResult[Tuple[ModelType, Any]] = await self.db.execute(
                clause.limit(limit).offset(skip),
            )
            
            # Execute query to get total count of items
            total_count_query = select(func.count()).select_from(clause.alias())
            result = await self.db.execute(total_count_query)
            total_count: int = result.fetchone()[0]

            
        except Exception:
            raise Exception("internal server error")

        return (
            list(map(tuple_first_item, list_obj)),
            total_count,
        )

    def sync_get_by_clause(
        self,
        clause: Select,
    ) -> Optional[ModelType]:
        try:
            obj_iter: ChunkedIteratorResult[
                Tuple[ModelType, Any]
            ] = self.db.execute(
                clause.limit(2).offset(0),
            )
        except Exception:
            raise Exception("internal server error")

        obj_list: list[ModelType] = list(
            map(tuple_first_item, obj_iter),
        )

        if len(obj_list) != 1:
            return None
        return obj_list[0]
    
    async def get_by_clause(
        self,
        clause: Select,
    ) -> Optional[ModelType]:
        try:
            obj_iter: ChunkedIteratorResult[
                Tuple[ModelType, Any]
            ] = await self.db.execute(
                clause.limit(2).offset(0),
            )
        except Exception:
            raise Exception("internal server error")

        obj_list: list[ModelType] = list(
            map(tuple_first_item, obj_iter),
        )

        if len(obj_list) != 1:
            return None
        return obj_list[0]
