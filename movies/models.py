from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255, blank=False, unique=True)
    director = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()

    # length in seconds
    length = models.IntegerField()


class Comment(models.Model):
    text = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
