from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('graph/', views.graph_view, name='graph_view'),
    path('graph/update_graph/', views.update_graph, name='update_graph'),
]