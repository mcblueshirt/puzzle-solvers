from src.game_board import GameBoard
from src.models import BoardLocation, Move


class InvalidMoveException(Exception):
    pass


VERTICAL_MOVE = (1, 0)
HORIZONTAL_MOVE = (0, 1)
FORWARD_DIAGONAL_MOVE = (-1, 1)
BACKWARD_DIAGONAL_MOVE = (1, 1)


class GameService:
    def __init__(self, disallowed_num_consecutive_chars: int = 4) -> None:
        self.disallowed_num_consecutive_chars = disallowed_num_consecutive_chars

    def make_move(self, game_board: GameBoard, new_move: Move) -> GameBoard:
        if self.is_valid_move(game_board, new_move):
            new_game_board = game_board.copy()
            new_game_board.update_cell(
                row_idx=new_move.cell.row_idx,
                col_idx=new_move.cell.col_idx,
                char=new_move.char,
            )
        else:
            raise InvalidMoveException()
        return new_game_board

    def is_valid_move(self, game_board: GameBoard, move: Move) -> bool:
        return (
            self.__is_within_board_boundaries(game_board, move.cell)
            and self.__is_empty_spot(game_board, move.cell)
            and self.__is_valid_num_consecutive_chars(game_board, move, VERTICAL_MOVE)
            and self.__is_valid_num_consecutive_chars(game_board, move, HORIZONTAL_MOVE)
            and self.__is_valid_num_consecutive_chars(
                game_board, move, FORWARD_DIAGONAL_MOVE
            )
            and self.__is_valid_num_consecutive_chars(
                game_board, move, BACKWARD_DIAGONAL_MOVE
            )
        )

    def __is_empty_spot(self, game_board: GameBoard, cell: BoardLocation) -> bool:
        return game_board.get_cell(row_idx=cell.row_idx, col_idx=cell.col_idx) == " "

    def __is_within_board_boundaries(
        self, game_board: GameBoard, loc: BoardLocation
    ) -> bool:
        return (
            0 <= loc.row_idx < game_board.n_rows
            and 0 <= loc.col_idx < game_board.n_cols
        )

    def __is_valid_num_consecutive_chars(
        self, game_board: GameBoard, move: Move, direction: tuple[int, int]
    ) -> bool:
        return (
            self.__count_consecutive_chars(
                game_board=game_board, move=move, direction=direction
            )
            < self.disallowed_num_consecutive_chars
        )

    def __count_consecutive_chars(
        self, game_board: GameBoard, move: Move, direction: tuple[int, int]
    ) -> int:
        temp_board = game_board.copy()
        temp_board.update_cell(
            row_idx=move.cell.row_idx, col_idx=move.cell.col_idx, char=move.char
        )

        count = 0
        for i in range(
            -1 * self.disallowed_num_consecutive_chars + 1,
            self.disallowed_num_consecutive_chars,
        ):
            current_row_idx = move.cell.row_idx + i * direction[0]
            current_col_idx = move.cell.col_idx + i * direction[1]
            if (
                0 <= current_row_idx < temp_board.n_rows
                and 0 <= current_col_idx < temp_board.n_cols
                and temp_board.get_cell(current_row_idx, current_col_idx) == move.char
            ):
                count += 1
                if count == self.disallowed_num_consecutive_chars:
                    return count
            else:
                count = 0
        return count
