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
    
    def perform_create(self, serializer):
        if serializer.is_valid():
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
                track = Track.objects.create(track_id = rec['id'], track_name = rec['name'], track_uri = rec['uri'], album_name = rec['album']['name'], 
                                             album_art = rec['album']['images'][0]['url'], album_release_date = rec['album']['release_date'], artist_id = rec['artists'][0]['id'],
                                             artist_name = rec['artists'][0]['name'], artist_uri = rec['artists'][0]['uri'])
                tracklist.append(track)
                track.save()
            
            recommendation = Recommendation.objects.create(user = self.request.user)
            recommendation.tracks.set(tracklist)
            recommendation.save()

            return Response({'message': 'Successfully got recommendations and added to database'}, status.HTTP_200_OK)

        else:
            return Response({'message': 'Error: ' + serializer.errors}, status.HTTP_400_BAD_REQUEST)

class RecommendationDeleteView(generics.DestroyAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recommendation.objects.filter(user = self.request.user)

# class RecommendationItemView(generics.ListAPIView, generics.RetrieveDestroyAPIView):
#     serializer_class = RecommendationItemSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         selected_recommendation = get_object_or_404(Recommendation, pk = self.kwargs.get('pk'))
#         return RecommendationItem.objects.filter(recommendation = selected_recommendation)

#     def destroy(self, request, *args, **kwargs):
#         selected_recommendation = get_object_or_404(Recommendation, pk = self.kwargs.get('pk'))
#         selected_recommendation.delete()
#         return Response({'message': "Deleted recommendation " + str(selected_recommendation.id)})