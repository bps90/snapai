from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('graph/', views.graph_view, name='graph_view'),
    path('graph/update_graph/', views.update_graph, name='update_graph'),
    path('graph/init_simulation/', views.init_simulation, name='init_simulation'),
    path('graph/run_simulation/', views.run_simulation, name='run_simulation'),
    path('graph/stop_simulation/', views.stop_simulation, name='stop_simulation'),
    path('graph/projects_names/', views.get_projects_names, name='projects_names'),
    path('graph/update_config/', views.update_config, name='update_config'),
    path('graph/get_config/', views.get_config, name='get_config'),
]