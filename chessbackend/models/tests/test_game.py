import pytest

from django.test import TestCase

from chessbackend.factories import GameFactory
from chessbackend.models.enums import ColorEnum, PieceTypeEnum


class GameLogicTests(TestCase):
    def setUp(self):
        self.game = GameFactory()

    def test_scholars_mate(self):
        self.game.start_game()
        self.game.refresh_from_db()

        pieces = self.game.pieces.all()
        expected_starting_piece_count = 32
        assert pieces.count() == expected_starting_piece_count

        # TODO implement scolars mate!
        # 1. grab the white e pawn and move 2 squares forward.
        white_e_pawn = pieces.get(
            color=ColorEnum.WHITE.value,
            current_column=4,
            current_row=1,
            type=PieceTypeEnum.PAWN.value,
        )
        self.game.move_piece(
            f"{white_e_pawn.current_column},{white_e_pawn.current_row}",
            f"{white_e_pawn.current_column},{white_e_pawn.current_row + 2}",
        )

        # 2. grab the black a pawn and move 2 squares forward.
        black_a_pawn = pieces.get(
            color=ColorEnum.BLACK.value,
            current_column=0,
            current_row=6,
            type=PieceTypeEnum.PAWN.value,
        )
        self.game.move_piece(
            f"{black_a_pawn.current_column},{black_a_pawn.current_row}",
            f"{black_a_pawn.current_column},{black_a_pawn.current_row - 1}",
        )

        # 3. grab the white light square bishop and move to c, 4
        white_light_square_bishop = pieces.get(
            color=ColorEnum.WHITE.value,
            current_column=5,
            current_row=0,
            type=PieceTypeEnum.BISHOP.value,
        )
        self.game.move_piece(
            f"{white_light_square_bishop.current_column},{white_light_square_bishop.current_row}",
            "2,3",
        )

        # 4. grab the black b pawn and move 1 square forward
        black_b_pawn = pieces.get(
            color=ColorEnum.BLACK.value,
            current_column=1,
            current_row=6,
            type=PieceTypeEnum.PAWN.value,
        )
        self.game.move_piece(
            f"{black_b_pawn.current_column},{black_b_pawn.current_row}",
            f"{black_b_pawn.current_column},{black_b_pawn.current_row - 1}",
        )

        # 5. grab the white queen and move to f, 3
        white_queen = pieces.get(
            color=ColorEnum.WHITE.value,
            current_column=3,
            current_row=0,
            type=PieceTypeEnum.QUEEN.value,
        )
        self.game.move_piece(
            f"{white_queen.current_column},{white_queen.current_row}", "5,2"
        )

        # 6. grab the black c pawn and move 1 square forward
        black_c_pawn = pieces.get(
            color=ColorEnum.BLACK.value,
            current_column=2,
            current_row=6,
            type=PieceTypeEnum.PAWN.value,
        )
        self.game.move_piece(
            f"{black_c_pawn.current_column},{black_c_pawn.current_row}",
            f"{black_c_pawn.current_column},{black_c_pawn.current_row - 1}",
        )

        # 7. grab the white queen and move to f, 7 for checkmate!
        white_queen.refresh_from_db()
        self.game.move_piece(
            f"{white_queen.current_column},{white_queen.current_row}", "5,6"
        )
        white_queen.refresh_from_db()

        pieces = self.game.pieces.all()
        self.game.refresh_from_db()

        # print(f"WHITE QUEEN IS DEFENDED: {white_queen.is_defended()}")
        # print(f"WHITE QUEEN CHECKING KING: {white_queen.is_checking_king()}")
        # print(f"WHITE QUEEN POSSIBLE MOVES: {white_queen.possible_moves()}")
        # print(f"WHITE QUEEN CURRENT COLUMN: {white_queen.current_column}")
        # print(f"WHITE QUEEN CURRENT ROW: {white_queen.current_row}")

        black_king = pieces.get(
            color=ColorEnum.BLACK.value, type=PieceTypeEnum.KING.value
        )
        # print(f"BLACK KING MOVES: {black_king.possible_moves()}")
        # print(f"BLACK KING CURRENT COLUMN: {black_king.current_column}")
        # print(f"BLACK KING CURRENT ROW: {black_king.current_row}")

        # print(f"BLACK KING IN CHECK: {game.black_in_check}")
        # print(f"BLACK KING IN CHECK: {game.black_check_pieces}")

        # print(f"GAME END TIME 2: {game.game_end_time}")
