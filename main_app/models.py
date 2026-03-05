from django.db import models
from django.urls import reverse

class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    year = models.IntegerField()
    rating = models.IntegerField()
    notes = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.title} - {self.artist}"

    def get_absolute_url(self):
        return reverse('album-detail', kwargs={'album_id': self.id})