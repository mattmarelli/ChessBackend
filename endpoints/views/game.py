from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from chessbackend.models import Game
from endpoints.serializers.game import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.actives.all()
    serializer_class = GameSerializer

    @action(detail=True, methods=["put"])
    def move_piece(self, request, pk):
        game = get_object_or_404(Game, pk=pk)

        # TODO at some point if the user making the request is not in the game
        # reject the request! Users not in the game should not be able to move pieces.
        start_position = request.data.get("start_position", None)
        end_position = request.data.get("end_position", None)
        print(f"START POSITION: {start_position}")
        print(f"END POSITION: {end_position}")
        if start_position and end_position:
            print("CALLING MOVE PIECE ON GAME OBJECT!")
            error = game.move_piece(start_position, end_position)
            if error:
                raise ValidationError(error)

            # TODO need to call the server sent event code here to update the connected parties!

        # game.move_piece()
        return Response(self.serializer_class(game).data, status=status.HTTP_200_OK)
