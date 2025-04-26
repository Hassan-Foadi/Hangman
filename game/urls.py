from django.urls import path
from .views import NewGameView, GameStatusView, MakeGuessView

urlpatterns = [
   path('game/new', NewGameView.as_view(), name='new_game'),
   path('game/<int:pk>', GameStatusView.as_view(), name='game_status'),
   path('game/<int:pk>/guess', MakeGuessView.as_view(), name='game_guess'),
]