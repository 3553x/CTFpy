from django.db import models

#Object representing a FAQ entry
class InfoPost(models.Model):
    title = models.CharField(max_length = 50)
    content = models.TextField()
    base = 'base.html'
    def __str__(self):
        return self.title
