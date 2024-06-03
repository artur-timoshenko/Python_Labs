from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=20)

class Player(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    position = models.CharField(max_length=20)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
