from datetime import datetime, UTC

from django.db import models
# from django.db.models.signals import pre_save
# from django.dispatch import receiver

from chessbackend.models.enums import ColorEnum, PieceTypeEnum, StartingPositionEnum

# Games will run on the server having the time remaining decrement
# Users clients will send requests to update the position of the pieces and status of the game

# Possible squares only 64!
# Game positions are (column, row)

# TODO maybe here soon remove tile_color from the dict here and make into its own CONSTANT!!!!!


def default_board():
    return {
        "0,0": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "0,1": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "0,2": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "0,3": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "0,4": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "0,5": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "0,6": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "0,7": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "1,0": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "1,1": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "1,2": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "1,3": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "1,4": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "1,5": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "1,6": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "1,7": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "2,0": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "2,1": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "2,2": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "2,3": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "2,4": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "2,5": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "2,6": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "2,7": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "3,0": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "3,1": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "3,2": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "3,3": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "3,4": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "3,5": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "3,6": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "3,7": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "4,0": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "4,1": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "4,2": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "4,3": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "4,4": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "4,5": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "4,6": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "4,7": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "5,0": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "5,1": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "5,2": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "5,3": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "5,4": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "5,5": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "5,6": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "5,7": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "6,0": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "6,1": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "6,2": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "6,3": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "6,4": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "6,5": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "6,6": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "6,7": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "7,0": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "7,1": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "7,2": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "7,3": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "7,4": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "7,5": {"piece": None, "tile_color": ColorEnum.BLACK.value},
        "7,6": {"piece": None, "tile_color": ColorEnum.WHITE.value},
        "7,7": {"piece": None, "tile_color": ColorEnum.BLACK.value},
    }


class Game(models.Model):
    game_start_time = models.DateTimeField(auto_now=True)
    game_end_time = models.DateTimeField(blank=True, null=True)
    initial_player_time = models.DurationField(blank=True, null=True)
    white_remaining_time = models.DurationField(blank=True, null=True)
    black_remaining_time = models.DurationField(blank=True, null=True)
    time_increment = models.IntegerField(blank=True, null=True)  # Time in seconds
    starting_position = models.CharField(
        max_length=25,
        choices=[
            (starting_position.value, starting_position.name)
            for starting_position in StartingPositionEnum
        ],
        default=StartingPositionEnum.STANDARD.value,
    )
    current_board = models.JSONField(
        default=dict
    )  # Dictionary to define the current game's status
    game_history = models.JSONField(
        default=dict
    )  # Dictionary to caputre the game's status at every move
    # TODO add users who are playing the game once I add that feature if I want to!

    white_in_check = models.BooleanField(default=False)
    white_check_pieces = models.JSONField(default=dict)
    black_in_check = models.BooleanField(default=False)
    black_check_pieces = models.JSONField(default=dict)

    def _initialize_standard_board(self):
        from chessbackend.models.piece import Piece

        self.current_board = default_board()
        created_pieces = []
        types_to_create = {
            0: PieceTypeEnum.ROOK.value,
            1: PieceTypeEnum.KNIGHT.value,
            2: PieceTypeEnum.BISHOP.value,
            3: PieceTypeEnum.QUEEN.value,
            4: PieceTypeEnum.KING.value,
        }
        for i in range(4):
            created_pieces.append(
                Piece.objects.create(
                    game=self,
                    color=ColorEnum.WHITE.value,
                    type=PieceTypeEnum.PAWN.value,
                    starting_row=1,
                    starting_column=i,
                    current_row=1,
                    current_column=i,
                )
            )
            created_pieces.append(
                Piece.objects.create(
                    game=self,
                    color=ColorEnum.WHITE.value,
                    type=PieceTypeEnum.PAWN.value,
                    starting_row=1,
                    starting_column=7 - i,
                    current_row=1,
                    current_column=7 - i,
                )
            )
            created_pieces.append(
                Piece.objects.create(
                    game=self,
                    color=ColorEnum.BLACK.value,
                    type=PieceTypeEnum.PAWN.value,
                    starting_row=6,
                    starting_column=i,
                    current_row=6,
                    current_column=i,
                )
            )
            created_pieces.append(
                Piece.objects.create(
                    game=self,
                    color=ColorEnum.BLACK.value,
                    type=PieceTypeEnum.PAWN.value,
                    starting_row=6,
                    starting_column=7 - i,
                    current_row=6,
                    current_column=7 - i,
                )
            )

            created_pieces.append(
                Piece.objects.create(
                    game=self,
                    color=ColorEnum.WHITE.value,
                    type=types_to_create[i],
                    starting_row=0,
                    starting_column=i,
                    current_row=0,
                    current_column=i,
                )
            )
            created_pieces.append(
                Piece.objects.create(
                    game=self,
                    color=ColorEnum.BLACK.value,
                    type=types_to_create[i],
                    starting_row=7,
                    starting_column=i,
                    current_row=7,
                    current_column=i,
                )
            )

            column_offset = i

            if i == 3:
                i = i + 1

            created_pieces.append(
                Piece.objects.create(
                    game=self,
                    color=ColorEnum.WHITE.value,
                    type=types_to_create[i],
                    starting_row=0,
                    starting_column=7 - column_offset,
                    current_row=0,
                    current_column=7 - column_offset,
                )
            )
            created_pieces.append(
                Piece.objects.create(
                    game=self,
                    color=ColorEnum.BLACK.value,
                    type=types_to_create[i],
                    starting_row=7,
                    starting_column=7 - column_offset,
                    current_row=7,
                    current_column=7 - column_offset,
                )
            )

        for created_piece in created_pieces:
            self.current_board[created_piece.current_position_string()]["piece"] = (
                created_piece.board_dict()
            )

        self.save()

    @classmethod
    def get_position_from_string(cls, string):
        column, row = [int(num) for num in string.split(",")]
        return (column, row)

    @classmethod
    def get_string_from_position(cls, position):
        return f"{position[0]},{position[1]}"

    def start_game(self):
        from chessbackend.models.move import Move

        if self.starting_position == StartingPositionEnum.STANDARD.value:
            self._initialize_standard_board()

        Move.objects.create(
            game=self,
            number=0,
            move_color=ColorEnum.WHITE.value,
        )

    def check_if_game_is_over(self):
        white_in_checkmate = self.check_king_in_checkmate(ColorEnum.WHITE.value)
        black_in_checkmate = self.check_king_in_checkmate(ColorEnum.BLACK.value)

        if white_in_checkmate:
            return ColorEnum.WHITE.value

        if black_in_checkmate:
            return ColorEnum.BLACK.value

        return

    def check_king_in_checkmate(self, king_color):
        # king = self.pieces.get(color=king_color, type=PieceTypeEnum.KING.value)
        if king_color == ColorEnum.WHITE.value:
            king_in_check = self.white_in_check
        else:
            king_in_check = self.black_in_check

        if not king_in_check:
            return False

        all_pieces = self.pieces.filter(color=king_color)
        for piece in all_pieces:
            if piece.possible_moves() != []:
                return False

        return True

    def end_game(self, game_over):
        self.game_end_time = datetime.now(UTC)

    def move_piece(self, starting_position: tuple, end_position: tuple) -> None:
        from chessbackend.models.move import Move

        current_move = self.moves.order_by("-number").first()
        starting_position_string = Game.get_string_from_position(starting_position)
        end_position_string = Game.get_string_from_position(end_position)
        end_time = datetime.now(UTC)
        moving_piece = self.current_board[starting_position_string]["piece"]
        ending_piece = self.current_board[end_position_string]["piece"]
        if ending_piece:
            end_p = self.pieces.get(id=ending_piece["id"])
            if moving_piece["piece_color"] == ending_piece["piece_color"]:
                return "Error.  Cannot move a piece onto a square of the same color"

        if current_move.move_color != moving_piece["piece_color"]:
            return "Error. Moving piece must be the same color as the move color"

        move_p = self.pieces.get(id=moving_piece["id"])

        current_move.moving_piece = move_p
        current_move.start_column = starting_position[0]
        current_move.start_row = starting_position[1]
        current_move.end_column = end_position[0]
        current_move.end_row = end_position[1]
        if ending_piece:
            current_move.captured_piece = end_p
        current_move.end_time = end_time
        current_move.save()

        move_p.current_column = end_position[0]
        move_p.current_row = end_position[1]
        if ending_piece:
            move_p.captured_piece = end_p
        move_p.save()

        self.current_board[starting_position_string]["piece"] = None
        self.current_board[end_position_string]["piece"] = move_p.board_dict()

        black_in_check = False
        white_in_check = False
        for piece in self.pieces.all():
            is_defended = piece.is_defended()
            if is_defended != piece.defended:
                piece.defended = is_defended
                piece.save()
                self.current_board[piece.current_position_string()]["piece"] = (
                    piece.board_dict()
                )

            is_checking_king = piece.is_checking_king()
            if piece.color == ColorEnum.BLACK.value:
                if is_checking_king:
                    white_in_check = True
                    self.white_in_check = True
                    self.white_check_pieces[piece.id] = piece.board_dict()
                else:
                    if piece.id in self.white_check_pieces:
                        del self.white_check_pieces[piece.id]
            else:
                if is_checking_king:
                    black_in_check = True
                    self.black_in_check = True
                    self.black_check_pieces[piece.id] = piece.board_dict()
                else:
                    if piece.id in self.black_check_pieces:
                        del self.black_check_pieces[piece.id]

        if not white_in_check and self.white_in_check:
            self.white_in_check = False
        if not black_in_check and self.black_in_check:
            self.black_in_check = False

        game_over = self.check_if_game_is_over()
        if game_over:
            self.end_game(game_over)
        self.save()

        Move.objects.create(
            game=self,
            number=current_move.number + 1,
            move_color=ColorEnum.BLACK.value
            if current_move.move_color == ColorEnum.WHITE.value
            else ColorEnum.WHITE.value,
        )
