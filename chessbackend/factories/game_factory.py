import factory

from chessbackend.models.game import Game


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game
