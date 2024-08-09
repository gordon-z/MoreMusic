from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Track(models.Model):
    track_id = models.CharField(db_index=True)
    track_name = models.CharField()
    track_uri = models.CharField()
    album_name = models.CharField()
    album_art = models.URLField()
    album_release_date = models.DateField()
    artist_id = models.CharField(db_index=True)
    artist_name = models.CharField()
    artist_uri = models.CharField()

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 255, blank=True)
    timestamp = models.DateTimeField(default=datetime.now)

class RecommendationItem(models.Model):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

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