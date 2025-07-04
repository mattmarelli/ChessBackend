from datetime import datetime, UTC

from django.db import models

from chessbackend.models.enums import ColorEnum, PieceTypeEnum, StartingPositionEnum
from chessbackend.models.move import Move
from chessbackend.models.piece import Piece
# Games will run on the server having the time remaining decrement
# Users clients will send requests to update the position of the pieces and status of the game

# Possible squares only 64!
# Game positions are (column, row)


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
    )
    current_board = models.JSONField(
        default={
            (0, 0): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (0, 1): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (0, 2): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (0, 3): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (0, 4): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (0, 5): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (0, 6): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (0, 7): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (1, 0): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (1, 1): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (1, 2): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (1, 3): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (1, 4): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (1, 5): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (1, 6): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (1, 7): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (2, 0): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (2, 1): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (2, 2): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (2, 3): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (2, 4): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (2, 5): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (2, 6): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (2, 7): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (3, 0): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (3, 1): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (3, 2): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (3, 3): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (3, 4): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (3, 5): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (3, 6): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (3, 7): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (4, 0): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (4, 1): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (4, 2): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (4, 3): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (4, 4): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (4, 5): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (4, 6): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (4, 7): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (5, 0): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (5, 1): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (5, 2): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (5, 3): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (5, 4): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (5, 5): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (5, 6): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (5, 7): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (6, 0): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (6, 1): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (6, 2): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (6, 3): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (6, 4): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (6, 5): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (6, 6): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (6, 7): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (7, 0): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (7, 1): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (7, 2): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (7, 3): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (7, 4): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (7, 5): {"piece": None, "tile_color": ColorEnum.BLACK.value},
            (7, 6): {"piece": None, "tile_color": ColorEnum.WHITE.value},
            (7, 7): {"piece": None, "tile_color": ColorEnum.BLACK.value},
        }
    )  # Dictionary to define the current game's status
    game_history = models.JSONField(
        default=dict
    )  # Dictionary to caputre the game's status at every move
    # TODO add users who are playing the game once I add that feature if I want to!

    def _create_standard_board(self):
        types_to_create = {
            0: PieceTypeEnum.ROOK.value,
            1: PieceTypeEnum.KNIGHT.value,
            2: PieceTypeEnum.BISHOP.value,
            3: PieceTypeEnum.QUEEN.value,
            4: PieceTypeEnum.KING.value,
        }
        for i in range(4):
            Piece.objects.create(
                game=self,
                color=ColorEnum.WHITE.value,
                type=PieceTypeEnum.PAWN.value,
                starting_row=1,
                starting_column=i,
                current_row=1,
                current_column=i,
            )
            Piece.objects.create(
                game=self,
                color=ColorEnum.WHITE.value,
                type=PieceTypeEnum.PAWN.value,
                starting_row=1,
                starting_column=7 - i,
                current_row=1,
                current_column=7 - i,
            )
            Piece.objects.create(
                game=self,
                color=ColorEnum.BLACK.value,
                type=PieceTypeEnum.PAWN.value,
                starting_row=6,
                starting_column=i,
                current_row=6,
                current_column=i,
            )
            Piece.objects.create(
                game=self,
                color=ColorEnum.BLACK.value,
                type=PieceTypeEnum.PAWN.value,
                starting_row=6,
                starting_column=7 - i,
                current_row=6,
                current_column=7 - i,
            )

            Piece.objects.create(
                game=self,
                color=ColorEnum.WHITE.value,
                type=types_to_create[i],
                starting_row=0,
                starting_column=i,
                current_row=0,
                current_column=i,
            )
            Piece.objects.create(
                game=self,
                color=ColorEnum.WHITE.value,
                type=types_to_create[i],
                starting_row=0,
                starting_column=7 - i,
                current_row=0,
                current_column=7 - i,
            )

            if i == 3:
                i = i + 1
            Piece.objects.create(
                game=self,
                color=ColorEnum.BLACK.value,
                type=types_to_create[i],
                starting_row=7,
                starting_column=i,
                current_row=7,
                current_column=i,
            )
            Piece.objects.create(
                game=self,
                color=ColorEnum.BLACK.value,
                type=types_to_create[i],
                starting_row=7,
                starting_column=7 - i,
                current_row=7,
                current_column=7 - i,
            )

    def start_game(self):
        if self.starting_position == StartingPositionEnum.STANDARD.name:
            self._create_standard_board()

        # TODO need to create the first move of the game for white!
        first_move = Move.objects.create(
            game=self,
            number=0,
        )
        # game = models.ForeignKey(Game, on_delete=models.SET_NULL, related_name="moves")
        # start_time = models.DateTimeField(auto_now=True)
        # end_time = models.DateTimeField(blank=True, null=True)
        # start_row = models.IntegerField()
        # start_column = models.IntegerField()
        # end_row = models.IntegerField()
        # end_column = models.IntegerField()
        # moving_piece = models.ForeignKey(
        #     Piece,
        #     on_delete=models.SET_NULL,
        #     related_name="moves",
        #     blank=True,
        #     null=True,
        # )
        # captured_piece = models.OneToOneField(
        #     Piece,
        #     on_delete=models.SET_NULL,
        #     related_name="capture_move",
        #     blank=True,
        #     null=True,
        # )
        # number = models.IntegerField()

    def move_piece(self, starting_position, end_position):
        current_move = self.moves.order_by("-number").first()
        end_time = datetime.now()
        moving_piece = self.current_board[starting_position]["piece"]
        ending_piece = self.current_board[end_position]["piece"]
        if ending_piece:
            if moving_piece.color == ending_piece.color:
                return "Error.  Cannot move a piece onto a square of the same color"
        
        current_move.moving_piece = moving_piece
        current_move.start_column = starting_position[0]
        current_move.start_row = starting_position[1]
        current_move.end_column = end_position[0]
        current_move.end_row = end_position[1]
        current_move.captured_piece = ending_piece
        current_move.save()

        # Move piece to end_position!
        moving_piece.column = end_position(0)
        moving_piece.row = end_position(1)
        moving_piece.captured_piece = ending_piece
        moving_piece.save()

        self.current_board[starting_position]["piece"] = None
        self.current_board[end_position]["piece"] = moving_piece