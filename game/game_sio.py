from flask_fullstack import EventController, EventSpace, DuplexEvent
from flask_socketio import join_room, leave_room

from common import User
from game.game_db import Game, GameUser
from game.utils import get_result_game

controller = EventController()


@controller.route()
class RoomEventSpace(EventSpace):

    @controller.jwt_authorizer(User)
    @controller.argument_parser(User.MainData)
    @controller.mark_duplex(Game.MainData, use_event=True)
    @controller.marshal_ack(Game.MainData)
    def start(self, event: DuplexEvent, user: User) -> str:
        game = Game.create()
        join_room(game.number)
        event.emit_convert(
            game,
            data={'room_code': game.number},
            room=game.number,
            include_self=True)

    @controller.jwt_authorizer(User)
    @controller.argument_parser(User.MainData)
    def join(self, user: User, number: str):
        join_room(number)

    @controller.jwt_authorizer(User)
    @controller.argument_parser(User.MainData)
    def leave(self, user: User, number: str):
        leave_room(number)

    def get_results(
        self,
        game_id: int,
        user_id: int,
        user_answer: str,
        enemy_id: int,
        enemy_answer: str
    ):
        game_user = GameUser.find_by_game_and_user_ids(game_id, user_id)
        game_enemy = GameUser.find_by_game_and_user_ids(game_id, enemy_id)
        game_user.result, game_enemy.result = get_result_game(
            user_answer, enemy_answer
        )

    @controller.jwt_authorizer(User)
    @controller.argument_parser()
    @controller.mark_duplex(GameUser.MainData, use_event=True)
    @controller.marshal_ack(GameUser.MainData)
    def make_shape_choice(
        self,
        event: DuplexEvent,
        game_id: int,
        number: str,
        user: User,
        answer: str
    ):
        game = GameUser.find_by_game_and_user_ids(game_id, user.id)
        game.answer = answer
        enemy = GameUser.get_enemy(game_id, user.id)
        enemys_answer = enemy.answer
        if enemys_answer:
            self.get_results(game_id, user.id, answer, enemy.id, enemys_answer)
            return event.emit_convert(
                game,
                room=number,
                include_self=True
            )
