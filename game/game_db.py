from __future__ import annotations
import random
import string

from flask_fullstack import PydanticModel, TypeEnum
from sqlalchemy import Column, select, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Enum
from sqlalchemy.orm import relationship

from common import User
from common.config import Base, db


class Answers(TypeEnum):
    ROCK = 'rock'
    PAPPER = 'papper'
    SCISSORS = 'scissors'

    @classmethod
    def list(cls) -> list:
        return [answer.value for answer in Answers]


class GameResults(TypeEnum):
    WIN = 1
    LOSE = -1
    TIE = 0


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

    @classmethod
    def get_all(cls, user_id: int) -> list | None:
        return db.session.query(cls).filter_by(user_id=user_id).all()


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
    answer: Column | Answers = Column(Enum(Answers))
    result: Column | GameResults = Column(Enum(GameResults))

    game: relationship = relationship(Game)
    user: relationship = relationship(User)

    MainData = PydanticModel.column_model(id, game_id, user_id, answer, result)
    AnswerModel = PydanticModel.column_model(answer)
    ResultModel = PydanticModel.column_model(result)

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
    def get_all(cls, user_id: int) -> GameUser | None:
        """Получение всех игр пользовальля."""
        return db.session.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def create(
        cls, game_id: int,
        user_id: int,
        answer: str,
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
