from requests import Response
from .models import Track, RecommendationItem, Recommendation
from .serializers import TrackSerializer, RecommendationItemSerializer, RecommendationSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Create your views here.

class TrackView(generics.RetrieveAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]


class RecommendationView(generics.ListCreateAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recommendation.objects.filter(user = self.request.user)
    
    def create(self, request, *args, **kwargs):
        type = request.data['seed_type']
        seed = request.data['seed']
        num_results = request.data['num_results']
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="7a45f115736c4d6e8e31ecaf6b03f2a9",
                                                           client_secret="206a8900c2e64d908d6e1beaf44c501a"))
        
        if type == "artists":
            output = sp.recommendations(seed_artists=seed, limit=num_results)
        elif type == "genres":
            output = sp.recommendations(seed_genres=seed, limit = num_results)
        elif type == "tracks":
            output = sp.recommendations(seed_tracks=seed, limit=num_results)

        recommendation = Recommendation.objects.create(user = request.user)

        for recc in output['tracks']:
            recommended_track = {recc['name']: [artist['name'] for artist in recc['artists']]}
            recommendation_item = RecommendationItem.objects.create(recommendation = recommendation, track = recommended_track)
            recommendation_item.save()

        return Response({'message': 'Successfully got recommendations and added to database'})
    

class RecommendationItemView(generics.ListAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecommendationItemSerializer
    permission_classes = [IsAuthenticated]