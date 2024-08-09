from rest_framework import serializers
from .models import Recommendation, RecommendationItem, Track
from django.contrib.auth.models import User

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'

class RecommendationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationItem
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'