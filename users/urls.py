from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import CustomTokenObtainPairView, CustomUserViewSet

urlpatterns = [
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/users/', CustomUserViewSet.as_view({'post': 'create'}), name='user_create'),
    path('auth/users/me/', CustomUserViewSet.as_view({
        'get': 'me',
        'patch': 'me',
    }), name='user_me'),
]
