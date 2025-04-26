from django.db import models

class Game(models.Model):
   word = models.CharField(max_length=50)
   guessed_letters = models.TextField(default="") #letters as a comma-seperated string
   wrong_guesses = models.IntegerField(default=0)
   max_wrong_guesses = models.IntegerField()
   
   
   STATUS_CHOICES = [
      ('InProgress', 'In Progress'),
      ('Won', 'Won'),
      ('Lost', 'Lost'),
   ]
   status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='InProgress')

   def __str__(self):
      return f"Game {self.id} - {self.status}"