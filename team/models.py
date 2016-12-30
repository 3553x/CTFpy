from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=50)
    unlocks = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class TeamMember(models.Model):
    member = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey('Team')
