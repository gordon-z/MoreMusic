from rest_framework.response import Response
from .models import Track, Recommendation
from .serializers import TrackSerializer, RecommendationSerializerPOST, RecommendationSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.contrib.auth.models import User
from decouple import config

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class TrackView(generics.RetrieveAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]


class RecommendationView(generics.ListCreateAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecommendationSerializerPOST
        else:
            return RecommendationSerializer
            
    def get_queryset(self):
        return Recommendation.objects.filter(user = self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'message': 'Successfully got recommendations and added to database'}, status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Error: ' + serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        seed_type = self.request.data['seed_type']
        seed = self.request.data['seed']
        num_results = self.request.data['num_results']
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = config('SPOTIFY_CLIENT_ID'),
                                                        client_secret = config('SPOTIFY_CLIENT_SECRET')))
        
        if seed_type == "artist":
            requested_artist = sp.search(q=seed, type=[seed_type], market="ca")
            artist_id = requested_artist['artists']['items'][0]['id']
            output = sp.recommendations(seed_artists=[artist_id], limit=num_results)
        elif seed_type == "genre":
            output = sp.recommendations(seed_genres=[seed], limit=num_results)
        elif seed_type == "track":
            requested_song = sp.search(q=seed, type=[seed_type], market="ca")
            song_id = requested_song['tracks']['items'][0]['id']
            output = sp.recommendations(seed_tracks=[song_id], limit=num_results)

        
        tracklist = []
        for rec in output['tracks']:

            track_id = rec['id']
            track_name = rec['name']
            track_uri = rec['uri']
            album_name = rec['album']['name']
            album_art = rec['album']['images'][0]['url']
            album_release_date = rec['album']['release_date']
            artist_id = rec['artists'][0]['id']
            artist_name = rec['artists'][0]['name']
            artist_uri = rec['artists'][0]['uri']
                
            track = Track.objects.create(track_id = track_id, track_name = track_name, track_uri = track_uri, album_name = album_name, 
                                         album_art = album_art, album_release_date = album_release_date, artist_id = artist_id, artist_name = artist_name, artist_uri = artist_uri)
            tracklist.append(track)
            track.save()
        
        recommendation = Recommendation.objects.create(user = self.request.user)
        recommendation.tracks.set(tracklist)
        recommendation.save()


class RecommendationDeleteView(generics.DestroyAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recommendation.objects.filter(user = self.request.user)

class RecommendationItemView(generics.RetrieveDestroyAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recommendation.objects.filter(user = self.request.user)
