from django.urls import path, include
from users.views import CustomTokenObtainPairView
from djoser.views import UserViewSet

urlpatterns = [
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/users/', UserViewSet.as_view({'post': 'create'}), name='user_create'),
    path('auth/users/me/', UserViewSet.as_view({
        'get': 'me',
        'patch': 'me',
    }), name='user_me'),
    path('auth/', include('djoser.urls.jwt')),
]
