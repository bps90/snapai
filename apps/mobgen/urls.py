from django.urls import path, include
from .views import HomeView, RandomWalkView, RandomWalkStreamingView

urlpatterns = [
    path('', HomeView.as_view()),
    path('RandomWalk/', RandomWalkView.as_view()),
    path('RandomWalk/streaming/', RandomWalkStreamingView.as_view()),
]