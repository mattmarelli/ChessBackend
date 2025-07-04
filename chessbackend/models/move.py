from django.db import models

from chessbackend.models.piece import Game, Piece


class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="moves")
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(blank=True, null=True)
    start_row = models.IntegerField(blank=True, null=True)
    start_column = models.IntegerField(blank=True, null=True)
    end_row = models.IntegerField(blank=True, null=True)
    end_column = models.IntegerField(blank=True, null=True)
    moving_piece = models.ForeignKey(
        Piece,
        on_delete=models.SET_NULL,
        related_name="moves",
        blank=True,
        null=True,
    )
    captured_piece = models.OneToOneField(
        Piece,
        on_delete=models.SET_NULL,
        related_name="capture_move",
        blank=True,
        null=True,
    )
    number = models.IntegerField()

    def movetime(self):
        return self.end_time - self.start_time
