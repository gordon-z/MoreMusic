from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('recommendation', views.RecommendationView.as_view()),
    path('recommendation/<int:id>', views.RecommendationItemView.as_view()),
    path('recommendation/delete/<int:pk>', views.RecommendationDeleteView.as_view()),
    path('user/register/', views.CreateUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]