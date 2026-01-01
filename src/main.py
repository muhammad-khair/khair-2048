import random
from typing import Callable, List

from src.game.board import GameBoard


def run_game_randomly(game: GameBoard) -> None:
    """
    Runs the game with random movements until game termination.

    :param game: GameBoard used to run
    """
    move_set: List[Callable[[], None]] = [
        game.move_left,
        game.move_right,
        game.move_up,
        game.move_down,
    ]
    while True:
        chosen_move: Callable[[], None] = random.choice(move_set)
        chosen_move()
        if game.status().is_terminal:
            break


def main() -> None:
    """Driver logic."""
    game = GameBoard.create_new()
    print("Initial grid:")
    print(game)

    print("\nRunning game now...")
    run_game_randomly(game)

    print(f"\nEnded game with {game.status()}:")
    print(game)
    print("Stats:")
    print(f"  - largest_number={game.largest_number()}")
    print(f"  - turns={game.turns}")


if __name__ == "__main__":
    main()
