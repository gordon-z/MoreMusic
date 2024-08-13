from django.urls import path
from . import views

urlpatterns = [
    path('recommendation', views.RecommendationView.as_view()),
    path('recommendation/<int:pk>', views.RecommendationItemView.as_view()),
]