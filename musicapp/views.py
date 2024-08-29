from requests import Response
from .models import Track, Recommendation
from .serializers import TrackSerializer, RecommendationSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.contrib.auth.models import User

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

    def get_queryset(self):
        return Recommendation.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            type = self.request.data['seed_type']
            seed = self.request.data['seed']
            num_results = self.request.data['num_results']
            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="7a45f115736c4d6e8e31ecaf6b03f2a9",
                                                            client_secret="206a8900c2e64d908d6e1beaf44c501a"))
            
            if type == "artists":
                output = sp.recommendations(seed_artists=seed, limit=num_results)
            elif type == "genres":
                output = sp.recommendations(seed_genres=seed, limit = num_results)
            elif type == "tracks":
                output = sp.recommendations(seed_tracks=seed, limit=num_results)

            
            tracklist = []
            for rec in output['tracks']:
                track = Track.objects.create(track_id = rec['id'], track_name = rec['name'], track_uri = rec['uri'], album_name = rec['album']['name'], 
                                             album_art = rec['album']['images'][0]['url'], album_release_date = rec['album']['release_date'], artist_id = rec['artists']['id'],
                                             artist_name = rec['artists']['name'], artist_uri = rec['artists']['uri'])
                tracklist.append(track)
                track.save()
                
            recommendation = Recommendation.objects.create(user = self.request.user, tracks = tracklist)
            recommendation.save()

            return Response({'message': 'Successfully got recommendations and added to database'})

        else:
            return Response({'message': 'Error: ' + serializer.errors})

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