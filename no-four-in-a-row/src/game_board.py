import csv
from prettytable import PrettyTable
from src.models import Move


class GameBoard:
    board: list[list[str]]
    n_rows: int
    n_cols: int

    def __init__(self, board: list[list[str]]) -> None:
        self.board = board
        self.n_rows = len(board)
        self.n_cols = len(board[0])

    @staticmethod
    def from_csv(board_path: str) -> "GameBoard":
        board = []
        with open(board_path, newline="") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                # Convert each row into a list and append to the board
                board.append(row)
        return GameBoard(board=board)

    @staticmethod
    def from_board(board: list[list[str]]) -> "GameBoard":
        return GameBoard(board=board)

    def get_cell(self, row_idx: int, col_idx: int) -> str:
        return self.board[row_idx][col_idx]

    def update_cell(self, row_idx: int, col_idx: int, char: str) -> None:
        self.board[row_idx][col_idx] = char

    def copy(self) -> "GameBoard":
        shallow_board = [row[:] for row in self.board]
        return GameBoard.from_board(board=shallow_board)

    def display_board(self, latest_move: Move | None = None) -> None:
        column_names = [" "] + [str(i) for i in range(len(self.board[0]))]
        table = PrettyTable(column_names)
        coloured_board = self.__colour_board(latest_move)
        for y, row in enumerate(coloured_board):
            table.add_row([y] + row)
        print(table)

    def __colour_board(self, latest_move: Move | None) -> list[list[str]]:
        coloured_board = []
        for row_idx, row in enumerate(self.board):
            coloured_row = []
            for col_idx, char in enumerate(row):
                is_latest = (
                    (row_idx, col_idx)
                    == (
                        latest_move.cell.row_idx,
                        latest_move.cell.col_idx,
                    )
                    if latest_move is not None
                    else False
                )
                coloured_row.append(self.__add_colour_to_char(char, is_latest))
            coloured_board.append(coloured_row)
        return coloured_board

    def __add_colour_to_char(self, char: str, is_latest: bool = False) -> str:
        char_colour_map = {"x": "red", "o": "blue", "latest": "green"}
        colour_ansi_map = {
            "red": "\033[91m",
            "blue": "\033[94m",
            "green": "\033[92m",
            "end": "\033[0m",
        }

        chosen_colour = (
            char_colour_map.get("latest", None)
            if is_latest
            else char_colour_map.get(char, None)
        )

        if chosen_colour is None:
            return char
        return (
            colour_ansi_map.get(chosen_colour, "")
            + char
            + colour_ansi_map.get("end", "")
        )
