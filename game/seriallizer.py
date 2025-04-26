from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
   class Meta:
      model = Game
      fields = [
         'id',
         'word',
         'guessed_letters',
         'wrong_guesses',
         'max_wrong_guesses',
         'status',
      ]
