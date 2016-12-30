from django.db import models
from django.contrib.auth.models import User
from team.models import Team

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Challenge(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    solution = models.CharField(max_length=255)
    eta = models.IntegerField(default=1)
    rank = models.IntegerField()
    cat = models.ForeignKey(Category, null=True)
    unlockedBy = models.ManyToManyField(Team, blank=True)
    class Meta:
        unique_together = ('rank', 'cat')
    def __str__(self):
        return self.name

class ChallengeFile(models.Model):
    remotePath = models.CharField(max_length=255)
    localPath = models.CharField(max_length=255)
    challenge = models.ForeignKey(Challenge)
    fileName = models.CharField(max_length=255)
    def __str__(self):
        return self.fileName + " - " + self.challenge.name


class Hint(models.Model):
    challenge = models.ForeignKey('Challenge')
    text = models.TextField()
    penalty = models.IntegerField()
    usedBy = models.ManyToManyField(Team, blank=True)
    def __str__(self):
        return str(self.challenge) + "(" + str(self.penalty) + ")"


class ChallengeSeen(models.Model):
    time = models.DateTimeField()
    team = models.ForeignKey(Team)
    challenge = models.ForeignKey('Challenge')
    def __str__(self):
        return str(self.challenge) + " -- " + str(self.team)

class SolvedChallenge(models.Model):
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    challenge = models.ForeignKey('Challenge')
    time = models.DateTimeField()
    points = models.IntegerField()
    totalPenalty = models.IntegerField()
    def __str__(self):
        return str(self.challenge) + " - " + str(self.team)

class WrongSubmisson(models.Model):
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    challenge = models.ForeignKey('Challenge')
    time = models.DateTimeField()
    text = models.TextField()
    def __str__(self):
        return str(self.user) + " - " + str(self.time)
