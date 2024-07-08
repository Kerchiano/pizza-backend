from django.urls import path, include

urlpatterns = [
    path('api/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
