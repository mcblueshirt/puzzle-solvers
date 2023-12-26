from src.game_board import GameBoard
from src.game_service import GameService
from src.solver_service import SolverService


def main() -> None:
    game_board = GameBoard.from_csv("boards/bigger-board.csv")
    solver_service = SolverService(game_service=GameService())

    solver_service.solve(game_board)


if __name__ == "__main__":
    main()
