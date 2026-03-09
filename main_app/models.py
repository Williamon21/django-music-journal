from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

LISTEN_TYPES = (
    ('F', 'Full listen'),
    ('P', 'Partial listen'),
    ('R', 'Re-listen'),
)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag-detail', kwargs={'pk': self.id})


class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    year = models.IntegerField()
    rating = models.IntegerField()
    notes = models.TextField(max_length=500)
    tags = models.ManyToManyField(Tag, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.artist}"

    def get_absolute_url(self):
        return reverse('album-detail', kwargs={'album_id': self.id})


class Listening(models.Model):
    date = models.DateField('Listening date')
    listen_type = models.CharField(
        max_length=1,
        choices=LISTEN_TYPES,
        default=LISTEN_TYPES[0][0]
    )
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_listen_type_display()} on {self.date}"

    class Meta:
        ordering = ['-date']


class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    spotify_id = models.CharField(max_length=100, blank=True)
    spotify_url = models.URLField(blank=True)
    preview_url = models.URLField(blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.artist}"
    
class Review(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.album.title}"

    class Meta:
        ordering = ['-created_at']