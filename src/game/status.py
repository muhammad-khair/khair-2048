from enum import Enum


class GameStatus(Enum):
    WIN = 0
    LOSE = 1
    ONGOING = 2

    @property
    def is_terminal(self) -> bool:
        match self:
            case GameStatus.WIN | GameStatus.LOSE:
                return True
            case _:
                return False
