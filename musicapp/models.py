from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recommendations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class RecommendationItem(models.Model):
    recommendations = models.ForeignKey(Recommendations, on_delete=models.CASCADE, related_name="recommendations")
    title = models.CharField(max_length = 255, blank=True)
    timestamp = models.DateTimeField(default=datetime.now)

class Track(models.Model):
    recommendation_item = models.ForeignKey(RecommendationItem, on_delete=models.CASCADE, related_name="recommendation_item")
    track_id = models.CharField()
    track_name = models.CharField()
    track_uri = models.CharField()
    album_name = models.CharField()
    album_art = models.URLField()
    album_release_date = models.DateField()
    artist_id = models.CharField()
    artist_name = models.CharField()
    artist_uri = models.CharField()

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