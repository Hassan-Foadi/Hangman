from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Game
from .seriallizer import GameSerializer

import random

WORDS = ["pen", "code", "python", "django", "hangman"]

class NewGameView(APIView):
   def post(self, request):
      word = random.choice(WORDS)
      max_wrong = len(word) - 1

      game = Game.objects.create(
         word = word,
         max_wrong_guesses = max_wrong,

      )

      serializer = GameSerializer(game)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
   

class GameStatusView(APIView):
   def get(self, request, pk):
      game = get_object_or_404(Game, pk=pk)

      #We build Partially guessed word
      display_word = ""
      for char in game.word:
         if char in game.guessed_letters:
            display_word += char

         else:
            display_word +="_"

      remaining_guesses = game.max_wrong_guesses - game.wrong_guesses

      return Response({
         "status": game.status,
         "word": display_word,
         "wrong_guesses": game.wrong_guesses,
         "remaining_guesses": remaining_guesses
      }) 
   
class MakeGuessView(APIView):
    def post(self, request, pk):
        game = get_object_or_404(Game, pk=pk)

        # Only stop if game is WON or LOST
        if game.status in ['Won', 'Lost']:
            return Response({"message": f"Game {game.status}."}, status=400)

        # Continue with normal guessing...

        letter = request.data.get('letter', '').lower()

        if not letter or len(letter) != 1 or not letter.isalpha():
            return Response({"error": "Invalid guess. Please enter a single letter."}, status=400)

        guessed = game.guessed_letters.split(',') if game.guessed_letters else []
        
        if letter in guessed:
            return Response({"message": "Letter already guessed."}, status=400)

        guessed.append(letter)
        game.guessed_letters = ','.join(guessed)

        if letter not in game.word:
            game.wrong_guesses += 1

        if all(c in guessed for c in game.word):
            game.status = 'Won'
        elif game.wrong_guesses >= game.max_wrong_guesses:
            game.status = 'Lost'

        game.save()

        return Response({
            "correct": letter in game.word,
            "status": game.status,
            "wrong_guesses": game.wrong_guesses,
            "guessed_letters": guessed
        }, status=200)
