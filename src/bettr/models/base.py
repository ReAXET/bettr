"""Base model for all models in the app."""

import re
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Type, Union
from sqlalchemy import inspect, select
from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel


class BaseModel(SQLModel, ABC):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(r'([a-z\d])([A-Z])', r'\1_\2', cls.__name__).lower()

    @classmethod
    def populate(cls, **kwargs) -> None:
        """Populates the database with the model's data."""
        raise NotImplementedError(
            f"Populate method not implemented for {cls.__name__}")

    @classmethod
    @property
    def primary_key(cls) -> str:
        """Returns the primary key for the model."""
        return inspect(cls).primary_key[0].name

    @classmethod
    @property
    def columns(cls) -> List[str]:
        """Returns the columns for the model."""
        return [column.name for column in inspect(cls).columns]

    @classmethod
    @property
    def relationships(cls) -> List[str]:
        """Returns the relationships for the model."""
        return [relationship.key for relationship in inspect(cls).relationships]

    @classmethod
    def save_dfs(cls, df):
        df_save = df.merge(
            cls.primary_key,
            how='left',
            indicator=True

        )
        df_save = df_save[df_save['_merge'] == 'left_only']

        if df_save.empty:
            logging.info(f"All primary keys already in {cls.__name__}")
            return

        columns_to_drop = set(df_save.columns) - \
            set(cls.__table__.columns.keys())
        df_save = df_save.drop(columns=columns_to_drop, axis=1)
        cls.model_validate(df_save)
        df_save.to_sql(
            cls.__tablename__,
            con=cls.db,
            if_exists='append',
            index=False
        )
        logging.info(f"Successfully saved {
                     len(df_save)} rows to {cls.__tablename__}")

    @classmethod
    def validate_df_model(cls, df) -> None:
        """Validates the model's data."""
        class DataFrameModel(BaseModel):
            __tablename__: str = cls.__tablename__
            __table__ = cls.__table__
            __database__ = cls.__database__
            __root__: list[cls]

        try:
            df_model = df.to_dict(orient='records')
            DataFrameModel.from_list(df_model)
        except Exception as e:
            raise ValueError(f"Validation failed for {cls.__name__}") from e
        logging.info(f"DataFrame validation passed for {cls.__name__}")

    @classmethod
    def model_validate(cls, model) -> None:
        """Validates the model's data."""
        try:
            cls.from_orm(model)
        except Exception as e:
            raise ValueError(f"Model validation failed for {
                             cls.__name__}") from e

        logging.info(f"Model validation passed for {cls.__name__}")

#   @classmethod
#   def get(cls, **kwargs) -> Optional[SQLModel]:
#       """Returns a single model from the database."""
#       return cls.db.execute(select(cls).filter_by(**kwargs)).first()
