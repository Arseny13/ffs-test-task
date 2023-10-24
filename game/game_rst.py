from flask_fullstack import ResourceController
from flask_restx import Resource
from flask_restx.reqparse import RequestParser

from common import User
from game.game_db import Game, GameUser, Answers


controller = ResourceController("game", path="/game/")

game_parser: RequestParser = RequestParser()
game_parser.add_argument("game_id", type=int, required=True)
game_parser.add_argument("user_id", type=int, required=True)


@controller.route("/answers/")
class Shape(Resource):

    @controller.jwt_authorizer(User)
    def get(self):
        """Получение списка всех доспутных ответов у игры."""
        return Answers.list()


@controller.route("/results/")
class GameResults(Resource):

    @controller.jwt_authorizer(User)
    @controller.argument_parser(game_parser)
    @controller.marshal_with(GameUser.ResultModel)
    def get(self, game_id: int, user_id: int):
        """Получение резльтата игры."""
        game = GameUser.find_by_game_and_user_ids(
            game_id=game_id,
            user_id=user_id
        )
        return game.result


@controller.route("/all/")
class Games(Resource):

    @controller.jwt_authorizer(User)
    @controller.marshal_with(Game.MainData)
    def get(self, user: User):
        """Получение свех игр пользователя."""
        return Game.get_all(user_id=user.id)
