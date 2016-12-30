from django.contrib import admin

from . import models

admin.site.register(models.Category)
admin.site.register(models.ChallengeFile)
admin.site.register(models.Challenge)
admin.site.register(models.Hint)

admin.site.register(models.ChallengeSeen)
admin.site.register(models.SolvedChallenge)
admin.site.register(models.WrongSubmisson)
