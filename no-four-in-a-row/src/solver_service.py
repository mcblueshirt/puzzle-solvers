from src.game_service import GameService
from src.game_board import GameBoard
from src.models import BoardLocation, Move
from src.decorators import timing_decorator  # type: ignore


class SolverService:
    game_service: GameService
    num_guesses: int = 0
    num_incorrect_guesses: int = 0
    num_board_states: int = 0

    def __init__(self, game_service: GameService) -> None:
        self.game_service = game_service

    @timing_decorator
    def solve(self, game_board: GameBoard) -> None:
        game_board.display_board()
        valid_move_map = self.__get_valid_move_map(game_board)

        is_solved, moves_made = self.__recursive_solve(
            game_board=game_board, valid_move_map=valid_move_map
        )
        if is_solved:
            self.__display_moves_made(game_board, moves_made)
        else:
            print("Invalid Board. Cannot be solved.")

    def __recursive_solve(
        self,
        game_board: GameBoard,
        valid_move_map: dict[str, list[Move]],
        previously_made_moves: list[Move] = [],
    ) -> tuple[bool, list[Move]]:
        while self.__forcible_moves_exist(valid_move_map):
            new_move = self.__get_forcible_move(valid_move_map)
            (
                game_board,
                previously_made_moves,
                valid_move_map,
            ) = self.__make_move_and_update_data(
                game_board=game_board,
                new_move=new_move,
                previously_made_moves=previously_made_moves,
            )

        if self.__is_solved(valid_move_map):
            return True, previously_made_moves
        if not self.__every_empty_space_has_valid_move(valid_move_map):
            self.num_incorrect_guesses += 1
            return False, []

        # No forcible moves left: make a guess
        for new_move in self.__flatten_valid_moves(valid_move_map):
            self.num_guesses += 1
            (
                new_game_board,
                new_previously_made_moves,
                new_valid_move_map,
            ) = self.__make_move_and_update_data(
                game_board=game_board,
                new_move=new_move,
                previously_made_moves=previously_made_moves,
            )
            is_solved, final_moves_made = self.__recursive_solve(
                game_board=new_game_board,
                valid_move_map=new_valid_move_map,
                previously_made_moves=new_previously_made_moves,
            )
            if is_solved:
                return True, final_moves_made
        return False, []

    def __get_valid_move_map(self, game_board: GameBoard) -> dict[str, list[Move]]:
        empty_spaces_valid_moves_dict = {}
        empty_cells = self.__get_empty_cells(game_board)
        for empty_cell in empty_cells:
            valid_moves = self.__valid_moves_for_cell(game_board, empty_cell)
            empty_spaces_valid_moves_dict[empty_cell.model_dump_json()] = valid_moves
        return empty_spaces_valid_moves_dict

    def __valid_moves_for_cell(
        self, game_board: GameBoard, cell: BoardLocation
    ) -> list[Move]:
        possible_moves = [
            Move(cell=cell, char="o"),
            Move(cell=cell, char="x"),
        ]
        valid_moves = [
            move
            for move in possible_moves
            if self.game_service.is_valid_move(game_board, move)
        ]
        return valid_moves

    def __forcible_moves_exist(self, valid_move_map: dict[str, list[Move]]) -> bool:
        for empty_cell in valid_move_map.keys():
            if len(valid_move_map[empty_cell]) == 1:
                return True
        return False

    def __get_forcible_move(self, valid_move_map: dict[str, list[Move]]) -> Move:
        for empty_cell in valid_move_map.keys():
            if len(valid_move_map[empty_cell]) == 1:
                return valid_move_map[empty_cell][0]
        raise Exception("No forcible move found")

    def __flatten_valid_moves(
        self, valid_move_map: dict[str, list[Move]]
    ) -> list[Move]:
        return [move for moves in valid_move_map.values() for move in moves]

    def __get_empty_cells(self, game_board: GameBoard) -> list[BoardLocation]:
        empty_cells: list[BoardLocation] = []
        for row_idx in range(game_board.n_rows):
            for col_idx in range(game_board.n_cols):
                if game_board.get_cell(row_idx, col_idx) == " ":
                    empty_cells.append(BoardLocation(row_idx=row_idx, col_idx=col_idx))
        return empty_cells

    def __every_empty_space_has_valid_move(
        self, valid_move_map: dict[str, list[Move]]
    ) -> bool:
        for empty_cell in valid_move_map.keys():
            if len(valid_move_map[empty_cell]) == 0:
                return False
        return True

    def __make_move_and_update_data(
        self,
        game_board: GameBoard,
        new_move: Move,
        previously_made_moves: list[Move],
    ) -> tuple[GameBoard, list[Move], dict[str, list[Move]]]:
        self.num_board_states += 1
        new_moves_made = previously_made_moves.copy() + [new_move]
        new_game_board = self.game_service.make_move(game_board, new_move)

        new_valid_move_map = self.__get_valid_move_map(new_game_board)

        return new_game_board, new_moves_made, new_valid_move_map

    def __is_solved(self, valid_move_map: dict[str, list[Move]]) -> bool:
        return len(valid_move_map.keys()) == 0

    def __display_moves_made(
        self, game_board: GameBoard, moves_made: list[Move]
    ) -> None:
        for move in moves_made:
            game_board = self.game_service.make_move(game_board, move)
            game_board.display_board(move)
        print("Game Complete. Solved")
        print(f"Number of board states analysed: {self.num_board_states}")
        print(f"Number of guesses: {self.num_guesses}")
        print(f"Number of incorrect guesses: {self.num_incorrect_guesses}")
