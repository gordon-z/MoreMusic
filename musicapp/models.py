from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Track(models.Model):
    track_id = models.CharField(max_length=255, db_index=True)
    track_name = models.CharField(max_length=255)
    track_uri = models.CharField(max_length=255)
    album_name = models.CharField(max_length=255)
    album_art = models.URLField()
    album_release_date = models.CharField(max_length=25)
    artist_id = models.CharField(max_length=255, db_index=True)
    artist_name = models.CharField(max_length=255)
    artist_uri = models.CharField(max_length=255)

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    tracks = models.ManyToManyField(Track)
    timestamp = models.DateTimeField(auto_now_add=True)
    seed_type = models.CharField(max_length=10)
    seed = models.CharField(max_length=255, db_index=True)


# class TrackAudioFeatures(models.Model):
#     track = models.OneToOneField(Track, on_delete=models.CASCADE, related_name="track")
#     acousticness = models.FloatField()
#     danceability = models.FloatField()
#     duration_ms = models.IntegerField()
#     energy = models.FloatField()
#     instrumentalness = models.FloatField()
#     key = models.IntegerField()
#     liveness = models.FloatField
#     loudness = models.FloatField()
#     mode = models.IntegerField()
#     speechiness = models.FloatField()
#     tempo = models.FloatField()
#     time_signature = models.IntegerField()
#     valence = models.FloatField()