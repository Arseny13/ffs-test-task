from __future__ import annotations
import enum
import random
import string

from flask_fullstack import PydanticModel, Identifiable
from sqlalchemy import Column, select, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy_utils.types import ChoiceType

from common.config import Base, db
from common import User


class ResultType(enum.Enum):
    ROCK = 'ROCK'
    PAPPER = 'PAPPER'
    SCISSORS = 'SCISSORS'


class Game(Base, Identifiable):
    """Таблица Игры."""
    __tablename__ = "games"
    not_found_text = "Game does not exist"
    unauthorized_error = (401, not_found_text)

    @staticmethod
    def generate_number() -> str:
        """
        Генерация случайного номера команты
        """
        return ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(16)
        )

    id: Column | int = Column(Integer, primary_key=True)
    number: Column | str = Column(String(16), unique=True, nullable=False)

    MainData = PydanticModel.column_model(id, number)

    @classmethod
    def find_by_id(cls, id: int) -> Game | None:
        """Поиск по id."""
        return db.get_first(select(cls).filter_by(id=id))

    @classmethod
    def find_by_number(cls, number: str) -> Game | None:
        """Поиск по номеру игры."""
        return db.get_first(select(cls).filter_by(number=number))

    @classmethod
    def create(cls, user: User) -> Game | None:
        """
        Создание игры.
        """
        return super().create(number=cls.generate_number())
