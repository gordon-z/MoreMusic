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
import google.generativeai as genai
import json

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
        return Recommendation.objects.filter(user = self.request.user).order_by('-timestamp')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            recommendation = self.perform_create(serializer)
            if recommendation.tracks.exists():
                return Response({'message': 'Successfully created recommendations and added to database'}, status.HTTP_201_CREATED)
            else:
                recommendation.delete()
                return Response({'message': 'No tracks found; recommendation deleted.'}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response({'message': 'Error: ' + serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        seed_type = self.request.data['seed_type']
        seed = self.request.data['seed']
        num_results = self.request.data['num_results']
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = config('SPOTIFY_CLIENT_ID'),
                                                        client_secret = config('SPOTIFY_CLIENT_SECRET')))
        
        genai.configure(api_key=config('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-2.0-flash')

        if seed_type == "artist":
            requested_artist = sp.search(q=seed, type=[seed_type], market="ca", limit=1)
            seed_name = requested_artist['artists']['items'][0]['name']
            seed_uri = requested_artist['artists']['items'][0]['uri']
        elif seed_type == "genre":
            output = sp.recommendations(seed_genres=[seed.lower()], limit=num_results)
        elif seed_type == "track":
            requested_song = sp.search(q=seed, type=[seed_type], market="ca", limit=1)
            seed_name = requested_song['tracks']['items'][0]['name']
            seed_uri = requested_song['tracks']['items'][0]['uri']
            
        prompt = f"Without previous context, given the following {seed_type} {seed_name} with URI {seed_uri}, provide {num_results} song recommendations based on similarity to your best estimate of the given seed's audio features. Make sure that the recommendations are within the same Spotify genre. Return output in format of JSON, with NO EXTRA text, with the following Spotify info: track_name, and artist_name fields."
        raw_response = model.generate_content(prompt).text
        # print(raw_response)
        raw_response = raw_response.replace("```json", "").replace("```", "").strip()
        responseJSON = json.loads(raw_response)
        
        output = {"tracks": []}
        for track in responseJSON:
            search_q = f"{track['track_name']} by {track['artist_name']}"
            track_info = sp.search(q=search_q, type=["track"], market="ca")
            output["tracks"].append(track_info)

        tracklist = []
        for track_info in output['tracks']:
            rec = track_info['tracks']['items'][0]
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
        
        recommendation = Recommendation.objects.create(user = self.request.user, seed_type = seed_type.title(), seed = seed)
        recommendation.tracks.set(tracklist)
        recommendation.save()
        
        return recommendation


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
