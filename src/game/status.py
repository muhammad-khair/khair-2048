from enum import Enum


class GameStatus(Enum):
    """
    Represents the current state of the game.

    This enum is used to determine whether the game is still in progress
    or has reached a terminal outcome (win or loss).
    """

    WIN = 0
    """The player has achieved a winning state."""

    LOSE = 1
    """The player has reached a losing state and can no longer make moves."""

    ONGOING = 2
    """The game is still in progress and moves can be made."""

    @property
    def is_terminal(self) -> bool:
        """
        Indicates whether the game has reached a terminal state.

        Returns:
            bool: ``True`` if the status is terminal else ``False``.
        """
        match self:
            case GameStatus.WIN | GameStatus.LOSE:
                return True
            case _:
                return False

    def __str__(self):
        return self.name
