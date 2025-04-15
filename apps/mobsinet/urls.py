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
    path('graph/add_nodes/', views.add_nodes, name='add_nodes'),
    path('graph/get_config/', views.get_config, name='get_config'),
    path('graph/calculate_degree/',
         views.calculate_degree, name='calculate_degree'),
    path('graph/calculate_diameter/',
         views.calculate_diameter, name='calculate_diameter'),
    path('graph/calculate_eccentricity/',
         views.calculate_eccentricity, name='calculate_eccentricity'),
    path('graph/calculate_shortest_path_between_two_nodes/',
         views.calculate_shortest_path_between_two_nodes, name='calculate_shortest_path_between_two_nodes'),
    path('graph/node2vec_algorithm/',
         views.node2vec_algorithm, name='node2vec_algorithm'),
    path('graph/calculate_distance/',
         views.calculate_distance, name='calculate_distance'),
    path('graph/reevaluate_connections/',
         views.reevaluate_connections, name='reevaluate_connections'),

]
