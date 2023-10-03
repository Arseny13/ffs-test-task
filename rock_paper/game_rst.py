from flask_fullstack import ResourceController
from flask_restx import Resource
from flask_restx.reqparse import RequestParser

from common import User
from rock_paper.game_db import Game, GameUser


controller = ResourceController("game", path="/game/")

game_parser: RequestParser = RequestParser()
game_parser.add_argument("game_id", type=int, required=True)
game_parser.add_argument("user_id", type=int, required=True)


@controller.route("/all/")
class Games(Resource):
    """Получение всех игр текущего пользоватлея."""

    @controller.jwt_authorizer(User)
    def get(self, user: User) -> GameUser:
        result = GameUser.get_all(user_id=user.id)
        return result
