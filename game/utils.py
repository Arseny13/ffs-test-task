from typing import Tuple

from game.game_db import Answers


def get_result_game(user_answer: str, enemy_answer: str) -> Tuple[str, str]:
    """Получение результата игра по ответам."""
    user_answer = user_answer.lower()
    enemy_answer = enemy_answer.lower()
    if user_answer == enemy_answer:
        return 'TIE', 'TIE'
    elif (
        user_answer == Answers.SCISSORS and enemy_answer == Answers.ROCK
    ) or (
        user_answer == Answers.PAPPER and enemy_answer == Answers.SCISSORS
    ) or (user_answer == Answers.ROCK and enemy_answer == Answers.PAPPER):
        return 'LOSE', 'WIN'
    else:
        return 'WIN', 'LOSE'
