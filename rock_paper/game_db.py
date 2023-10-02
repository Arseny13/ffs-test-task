from __future__ import annotations
import enum
import random
import string

from flask_fullstack import PydanticModel
from sqlalchemy import Column, select, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy_utils.types import ChoiceType

from common.config import Base, db


class AnswerType(enum.Enum):
    ROCK = 'ROCK'
    PAPPER = 'PAPPER'
    SCISSORS = 'SCISSORS'


class Game(Base):
    """Таблица Игры."""
    __tablename__ = "games"
    not_found_text = "Game does not exist"

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
    def create(cls, game_id: int) -> Game | None:
        """
        Создание игры.
        """
        return super().create(
            game_id=game_id,
            number=cls.generate_number()
        )


class GameUser(Base):
    """Таблица Игры c пользователем."""
    __tablename__ = "games_users"
    not_found_text = "GameUser does not exist"

    id: Column | int = Column(Integer, primary_key=True)
    game_id: Column | int = Column(
        Integer,
        ForeignKey('games.id'),
        nullable=False
    )
    user_id: Column | int = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False
    )
    answer: Column | AnswerType = Column(ChoiceType(AnswerType))
    result: Column | str = Column(String(4))

    MainData = PydanticModel.column_model(id, game_id)

    @classmethod
    def find_by_id(cls, game_id: int, user_id: int) -> GameUser | None:
        """Поиск по id."""
        return db.get_first(
            select(cls).filter_by(
                game_id=game_id,
                user_id=user_id
            )
        )

    @classmethod
    def find_enemy(cls, game_id: int, user_id: int) -> GameUser | None:
        """Поиск противника в той же игре."""
        return db.get_first(
            select(cls).where(
                game_id == game_id,
                user_id != user_id
            )
        )

    @classmethod
    def create(
        cls, game_id: int,
        user_id: int, answer: str,
        result: str
    ) -> GameUser | None:
        """
        Создание игры c пользователем.
        """
        return super().create(
            game_id=game_id,
            user_id=user_id,
            answer=answer,
            result=result
        )
