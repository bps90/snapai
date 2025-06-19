from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from .simulator.network_simulator import simulation
import json
from networkx.readwrite import json_graph
from .simulator.global_vars import Global
import os
from django.views.decorators.csrf import csrf_exempt
from .simulator.main import Main
import networkx as nx
from .simulator.models.nodes.abc_node import AbcNode
from node2vec import Node2Vec  # type: ignore
import numpy as np
import gensim  # type: ignore
from .simulator.configuration.sim_config import SimulationConfig
from .simulator.asynchronous_thread import AsynchronousThread
from .simulator.gnn.link_prediction_gnn import LinkPredictionGNN
from .simulator.gnn.node_clusterization_gnn import NodeClusterizationGNN, NodeClusterizationDBSCAN
from .simulator.gnn.node_classification_gnn import NodeClassificationGNN
from math import pi
from .simulator.tools.models_search_engine import ModelsSearchEngine
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from typing import cast, Any, Literal
from .simulator.projects.sample9.nodes.s9_node import S9Node
from .simulator.projects.sample9.connectivity_models.s9_connectivity import S9Connectivity
from .simulator.defaults.distribution_models.circular_dist import CircularDistParameters
from .simulator.projects.sample9.mobility_models.midpoint_waypoint import MidpointWaypointParameters
from .simulator.projects.sample9.mobility_models.mid_point_of_others import MidPointOfOthersParameters
from .simulator.defaults.mobility_models.random_walk import RandomWalkParameters
import importlib
from .simulator.configuration.base_project_config import BaseProjectConfig
from .simulator.models.abc_model import AbcModel


def index(request):
    return render(request, "mobsinet_index.html")


def graph_view(request):
    return render(request, 'graph.html', {"projects": os.listdir(SimulationConfig.PROJECTS_DIR)})


def update_graph(request):
    with_logs = request.GET.get('with_logs') == 'true'
    node_link_data = json_graph.node_link_data(
        simulation.graph, edges="edges")  # type: ignore

    # [id, x, y, z, size, color]
    nodes = list(map(lambda node: [node['id'].id,
                                   node['id'].position.x,
                                   node['id'].position.y,
                                   node['id'].position.z,
                                   node['id'].size,
                                   node['id'].node_color.get_hex()],
                     node_link_data.get('nodes')))
    links: list[list[int]] = []

    for link in node_link_data.get('edges'):
        # [source, target, bidirectional]
        opposite = [link['target'].id, link['source'].id, 0]
        try:
            opposite_index = links.index(opposite)
            links[opposite_index][2] = 1
        except ValueError:
            links.append([link['source'].id, link['target'].id, 0])

    graph_data = {
        'msg_r': Global.number_of_messages_in_this_round,
        'msg_a': Global.number_of_messages_over_all,
        't': Global.current_time,
        'r': Global.is_running,
        'n': nodes,
        'l': links,
        'logs': Global.round_logs if with_logs else [],
    }

    return JsonResponse(graph_data)


def convert_keys_to_strings(input_dict):
    if isinstance(input_dict, dict):
        return {str(key): convert_keys_to_strings(value)
                for key, value in input_dict.items()}
    elif isinstance(input_dict, list):
        return [convert_keys_to_strings(item) for item in input_dict]
    else:
        return input_dict


def get_projects_names(request):
    return JsonResponse(os.listdir(SimulationConfig.PROJECTS_DIR), safe=False)


def init_simulation(request):
    project = request.GET.get('project')

    Main.init(project)

    return HttpResponse(status=200)


def reevaluate_connections(request):
    AsynchronousThread.reevaluate_connections()

    return HttpResponse(status=200)


def run_simulation(request):
    rounds = int(request.GET.get('rounds'))
    refresh_rate = float(request.GET.get('refresh_rate'))

    simulation.run(rounds, refresh_rate)

    return HttpResponse(status=200)


def stop_simulation(request):
    if (simulation.running_thread):
        simulation.stop()

    return HttpResponse(status=200)


@csrf_exempt
def update_config(request: HttpRequest):
    if request.method == "POST":
        try:
            # Carrega os dados enviados no formulário
            form_data = request.POST.dict()

            # Carrega o JSON existente
            with open(os.path.join(SimulationConfig.PROJECTS_DIR, form_data['project'], 'config.json'), "r") as json_file:
                existing_data = json.load(json_file)

            # Atualiza os dados existentes com os dados do formulário
            updated_data = merge_data(existing_data, form_data)

            # Salva o JSON atualizado no arquivo
            with open(os.path.join(SimulationConfig.PROJECTS_DIR, form_data['project'], 'config.json'), "w") as json_file:
                json.dump(updated_data, json_file, indent=4)

            # Retorna uma resposta de sucesso
            return JsonResponse({"status": "success", "message": "JSON atualizado com sucesso!"})
        except Exception as e:
            # Retorna uma resposta de erro
            print(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse("Método não permitido", status=405)


def get_config_form_layout(request: HttpRequest):
    project_name = request.GET.get('project')

    if (project_name is None):
        return HttpResponse(status=400, content="Project name not provided")

    try:
        ProjectConfig: BaseProjectConfig = importlib.import_module(
            SimulationConfig.PROJECTS_DIR.replace('/', '.') + project_name + '.project_config').ProjectConfig

        return JsonResponse({
            "simulation_config_layout": SimulationConfig.get_form_layout().to_dict(),
            "project_config_layout": ProjectConfig.get_form_layout().to_dict()
        })
    except ModuleNotFoundError as e:
        return JsonResponse({
            "simulation_config_layout": SimulationConfig.get_form_layout().to_dict(),
            "project_config_layout": None
        })
    except Exception as e:
        print(e)
        return HttpResponse(status=500, content="See backend console for more details")


def get_model_subsection_layout(request: HttpRequest):
    model_name = request.GET.get('model')
    model_type = request.GET.get('model_type')

    if (model_name is None):
        return HttpResponse(status=400, content="Model name not provided")

    if (model_type is None or model_type not in ['connectivity', 'mobility', 'interference', 'reliability', 'distribution', 'message_transmission']):
        return HttpResponse(status=400, content="Invalid model type")

    try:
        Model = ModelsSearchEngine.find_model(model_name, cast(Literal['connectivity', 'mobility', 'interference', 'reliability',
                                                                       'distribution', 'message_transmission'], model_type))

        return JsonResponse({"model_subsection_layout": Model.form_subsection_layout.to_dict() if 'form_subsection_layout' in Model.__dict__ else None})
    except ModuleNotFoundError as e:
        return HttpResponse(status=404, content="Model not found")
    except Exception as e:
        print(e)
        return HttpResponse(status=500, content="See backend console for more details")


def merge_data(existing_data, form_data):
    """
    Atualiza os dados existentes com base nos dados do formulário.
    Converte os dados do formulário em tipos apropriados.
    """
    for key, value in form_data.items():
        # Trata chaves aninhadas (ex.: network_parameters[type] -> network_parameters['type'])
        if "[" in key and "]" in key:
            keys = key.replace("]", "").split("[")
            sub_data = existing_data
            for sub_key in keys[:-1]:
                sub_data = sub_data.setdefault(sub_key, {})
            sub_data[keys[-1]] = parse_value(value)
        else:
            # Atualiza diretamente se for uma chave simples
            existing_data[key] = parse_value(value)
    return existing_data


def parse_value(value):
    """
    Converte strings em tipos apropriados (int, float, bool, listas ou strings).
    """
    if (value == ""):
        return None
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        if value.lower() in ["true", "false"]:
            return value.lower() == "true"
        elif "," in value:  # Trata listas separadas por vírgulas
            return [parse_value(v.strip()) for v in value.split(",")]
        return value


def get_config(request):
    """
    Lê um arquivo JSON existente e retorna os dados como resposta.
    """

    try:
        # Lê o arquivo JSON
        with open(os.path.join(SimulationConfig.PROJECTS_DIR, request.GET.get('project'), 'config.json'), "r") as json_file:
            data = json.load(json_file)

        # Retorna os dados em formato JSON
        return JsonResponse(data, safe=False)
    except FileNotFoundError:
        # Retorna um erro se o arquivo não for encontrado
        return JsonResponse({"error": "Arquivo JSON não encontrado."}, status=404)
    except json.JSONDecodeError:
        # Retorna um erro se o JSON for inválido
        return JsonResponse({"error": "Erro ao decodificar o arquivo JSON."}, status=500)


def calculate_degree(request):
    node_id = request.GET.get('node_id')

    if (node_id == "" or not node_id.isdigit()):
        return JsonResponse({"message": "ID inválido."}, status=400)

    node = simulation.get_node_by_id(int(node_id))

    if not isinstance(node, AbcNode):
        return JsonResponse({"message": "Não encontrado."}, status=404)

    try:
        degree = simulation.graph.degree(node)

        return JsonResponse({"degree": degree})
    except Exception as e:
        print(e)
        return JsonResponse({"message": e.args}, status=400)


def calculate_diameter(request):
    try:
        diameter = nx.diameter(simulation.graph)
        return JsonResponse({"diameter": diameter})
    except Exception as e:
        print(e)
        return JsonResponse({"message": e.args}, status=400)


def calculate_eccentricity(request):
    node_id = request.GET.get('node_id')

    if (node_id == "" or not node_id.isdigit()):
        return JsonResponse({"message": "ID inválido."}, status=400)

    node = simulation.get_node_by_id(int(node_id))

    if not isinstance(node, AbcNode):
        return JsonResponse({"message": "Não encontrado."}, status=404)

    try:
        eccentricity: int = nx.eccentricity(simulation.graph, node)

        return JsonResponse({"eccentricity": eccentricity})
    except Exception as e:
        print(e)
        return JsonResponse({"message": e.args}, status=400)


def calculate_shortest_path_between_two_nodes(request):
    node1_id = request.GET.get('node1_id')
    node2_id = request.GET.get('node2_id')

    if (node1_id == "" or not node1_id.isdigit() or node2_id == "" or not node2_id.isdigit()):
        return JsonResponse({"message": "ID inválido."}, status=400)

    node1 = simulation.get_node_by_id(int(node1_id))
    node2 = simulation.get_node_by_id(int(node2_id))

    if not isinstance(node1, AbcNode) or not isinstance(node2, AbcNode):
        return JsonResponse({"message": "Não encontrado."}, status=404)

    try:
        shortest_path: list = nx.shortest_path(
            simulation.graph, node1, node2)

        return JsonResponse({"shortest_path": [node.id for node in shortest_path]})
    except Exception as e:
        print(e)
        return JsonResponse({"message": e.args}, status=400)


def new_fit_for_node2vec(self, **skip_gram_params):
    """
    Creates the embeddings using gensim's Word2Vec.
    :param skip_gram_params: Parameteres for gensim.models.Word2Vec - do not supply 'size' it is taken from the Node2Vec 'dimensions' parameter
    :type skip_gram_params: dict
    :return: A gensim word2vec model
    """

    if 'workers' not in skip_gram_params:
        skip_gram_params['workers'] = self.workers

    if 'vector_size' not in skip_gram_params:
        skip_gram_params['vector_size'] = self.dimensions

    return gensim.models.Word2Vec(self.walks, **skip_gram_params)


def node2vec_algorithm(request):
    dimensions = request.GET.get('dimensions')

    if (dimensions == "" or not dimensions.isdigit()):
        return JsonResponse({"message": "Invalid dimensions."}, status=400)

    node2vec = Node2Vec(
        simulation.graph, dimensions=int(dimensions), workers=1)

    # For compatibility with the project version of gensim
    node2vec.fit = new_fit_for_node2vec

    model = node2vec.fit(node2vec, window=10, min_count=1, batch_words=4)

    model.wv.save_word2vec_format(
        f'{SimulationConfig.PROJECTS_DIR}{Global.project_name}/node2vec-{SimulationConfig.simulation_name}-{dimensions}D.emb')

    # Obtém os nós e os vetores
    words = list(model.wv.index_to_key)  # Lista de nós
    vectors = np.array([model.wv[word]
                       for word in words])  # Vetores (já em 2D)

    return JsonResponse({"words": words, "vectors": vectors.tolist()})


@csrf_exempt
def add_nodes(request):
    if request.method == "POST":

        # Carrega os dados enviados no formulário
        form_data = parse_nested_dict(request.POST.dict())

        simulation.add_nodes(
            num_nodes=int(form_data['num_nodes']),
            distribution_model_arg=form_data['distribution_model'],
            node_arg=form_data['node'],
            mobility_model_arg=form_data['mobility_model'],
            connectivity_model_arg=form_data['connectivity_model'],
            interference_model_arg=form_data['interference_model'],
            reliability_model_arg=form_data['reliability_model'],
            node_color=form_data['node_color'],
            node_size=int(form_data['node_size']),
            distribution_model_parameters=form_data['distribution_model_parameters'],
            mobility_model_parameters=form_data['mobility_model_parameters'],
            connectivity_model_parameters=form_data['connectivity_model_parameters'],
            interference_model_parameters=form_data['interference_model_parameters'],
            reliability_model_parameters=form_data['reliability_model_parameters'],
        )

        # Retorna uma resposta de sucesso
        return JsonResponse({"status": "success", "message": "JSON atualizado com sucesso!"})

    else:
        return HttpResponse("Método não permitido", status=405)


def parse_nested_dict(flat_dict):
    nested_dict: dict[str, Any] = {}

    for key, value in flat_dict.items():
        # Divide os parâmetros aninhados
        keys = key.replace("]", "").split("[")
        current_level = nested_dict

        for part in keys[:-1]:  # Percorre os níveis do dicionário
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

        # Converte valores numéricos e booleanos
        if value.isdigit():
            value = int(value)
        elif value.replace(".", "", 1).isdigit():
            value = float(value)
        elif value.lower() in ["true", "false"]:
            value = value.lower() == "true"
        elif "," in value:
            value = value.split(",")
            value = [int(v) if v.isdigit() else float(v) if v.replace(
                ".", "", 1).isdigit() else v for v in value]

        current_level[keys[-1]] = value

    return nested_dict


def calculate_distance(request):
    node1_id = request.GET.get('node1')
    node2_id = request.GET.get('node2')

    if (node1_id == "" or not node1_id.isdigit() or node2_id == "" or not node2_id.isdigit()):
        return JsonResponse({"message": "ID inválido."}, status=400)

    node1 = simulation.get_node_by_id(int(node1_id))
    node2 = simulation.get_node_by_id(int(node2_id))

    if not isinstance(node1, AbcNode) or not isinstance(node2, AbcNode):
        return JsonResponse({"message": "Não encontrado."}, status=404)

    return JsonResponse({"distance": node1.position.euclidean_distance(node2.position)})


class Static:
    metrics_model_filtered_path = f'{SimulationConfig.PROJECTS_DIR}sample9/...'


def train_link_prediction(request):
    lpgnn = LinkPredictionGNN()
    graph = LinkPredictionGNN.transform_graph_of_objects_to_graph_of_integers(
        simulation.graph)
    features = LinkPredictionGNN.get_features_from_file(
        Static.metrics_model_filtered_path)
    labels = [(node.id, int(str(cast('S9Node', node).company_id) + str(cast('S9Node', node).platoon_id)))
              for node in simulation.nodes()]

    lpgnn.create_dataset(graph, features, labels)

    lpgnn.train()

    lpgnn.save()

    return JsonResponse({"status": "success", "message": "dataset criado com sucesso!"})


def predict_links(request):
    lpgnn = LinkPredictionGNN()
    lpgnn.load()

    predictions = lpgnn.predict_edges_above_threshold_in_new_graph(simulation.graph, LinkPredictionGNN.get_features_from_file(
        Static.metrics_model_filtered_path))

    return JsonResponse({"status": "success", "data": predictions})


def train_node_clusterization(request: HttpRequest):
    n_clusters = int(request.GET.get('n_clusters') or '2')

    ncgnn = NodeClusterizationGNN()

    graph = LinkPredictionGNN.transform_graph_of_objects_to_graph_of_integers(
        simulation.graph)
    features = LinkPredictionGNN.get_features_from_file(
        Static.metrics_model_filtered_path)

    ncgnn.create_dataset(graph, features)

    ncgnn.train_encoder(in_channels=11, hidden_channels=32)

    # clusters = ncgnn.cluster_nodes(eps=0.001, min_samples=5).tolist()

    clusters: list[int] = ncgnn.cluster_nodes(n_clusters).tolist()

    clusters_info = []

    for i in range(n_clusters):
        nodes_in_cluster = list(map(lambda x: x[0].id,
                                    filter(lambda x: x[1] == i, zip(simulation.nodes(), clusters))))

        clusters_info.append({
            "cluster": i,
            "nodes": clusters.count(i),
            "normal_nodes": len(list(filter(lambda x: x <= 157, nodes_in_cluster))) / len(nodes_in_cluster) * 100,
            "intruder_nodes": len(list(filter(lambda x: x > 157, nodes_in_cluster))) / len(nodes_in_cluster) * 100
        })

    return JsonResponse({"status": "success", "clusters_info": clusters_info, "num_clusters": n_clusters, "clusters": clusters})


def train_node_clusterization_dbscan(request: HttpRequest):
    eps = float(request.GET.get('eps') or '0.001')
    minPts = int(request.GET.get('minPts') or '5')

    ncgnn = NodeClusterizationDBSCAN()

    graph = LinkPredictionGNN.transform_graph_of_objects_to_graph_of_integers(
        simulation.graph)
    features = LinkPredictionGNN.get_features_from_file(
        Static.metrics_model_filtered_path)

    ncgnn.create_dataset(graph, features)

    ncgnn.train_encoder(in_channels=11, hidden_channels=32)

    clusters: list[int] = ncgnn.cluster_nodes(
        eps=eps, min_samples=minPts).tolist()

    n_clusters = max(clusters) - min(clusters) + 1

    clusters_info = []

    for i in range(min(clusters), max(clusters) + 1):
        nodes_in_cluster = list(map(lambda x: x[0].id,
                                    filter(lambda x: x[1] == i, zip(simulation.nodes(), clusters))))

        clusters_info.append({
            "cluster": i,
            "nodes_in_cluster": nodes_in_cluster,
            "nodes": clusters.count(i),
            "normal_nodes": len(list(filter(lambda x: x <= 157, nodes_in_cluster))) / len(nodes_in_cluster) * 100,
            "intruder_nodes": len(list(filter(lambda x: x > 157, nodes_in_cluster))) / len(nodes_in_cluster) * 100
        })

    return JsonResponse({"status": "success", "clusters_info": clusters_info, "num_clusters": n_clusters, "clusters": clusters})


def train_node_classification(request):
    binary = request.GET.get('binary') == 'true'
    epochs = int(request.GET.get('epochs') or '1000')

    ncgnn = NodeClassificationGNN()
    graph = LinkPredictionGNN.transform_graph_of_objects_to_graph_of_integers(
        simulation.graph)
    features = LinkPredictionGNN.get_features_from_file(
        Static.metrics_model_filtered_path)
    labels = [(node.id, (1 if cast('S9Node', node).company_id else 0) if binary else cast('S9Node', node).company_id)
              for node in simulation.nodes()]

    ncgnn.create_dataset(graph, features, labels)

    ncgnn.train(epochs=epochs)

    ncgnn.save()

    return JsonResponse({"status": "success", "message": "dataset criado com sucesso!"})


def classificate_nodes(request):
    binary = request.GET.get('binary') == 'true'

    ncgnn = NodeClassificationGNN()
    ncgnn.load()
    graph = LinkPredictionGNN.transform_graph_of_objects_to_graph_of_integers(
        simulation.graph)
    features = LinkPredictionGNN.get_features_from_file(
        Static.metrics_model_filtered_path
    )

    predictions = ncgnn.predict_node_labels(graph, LinkPredictionGNN.get_features_from_file(
        Static.metrics_model_filtered_path))

    labels = [(node.id, (1 if cast('S9Node', node).company_id else 0) if binary else cast('S9Node', node).company_id)
              for node in simulation.nodes()]

    y_true = [label for _, label in labels]

    predictions = ncgnn.predict_node_labels(graph, features)
    y_pred = [label for _, label in predictions]

    acc = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred, output_dict=True)
    matrix = confusion_matrix(y_true, y_pred).tolist()  # para JSON

    result = [{"node": int(node + 1), "label": int(label)}
              for node, label in predictions]

    info = {
        "accuracy": acc,
        "report": report,
        "confusion_matrix": matrix
    }

    return JsonResponse({"status": "success", "data": result, "info": info})


def network_configuration1(request):
    """
    Initialize project sample9
    Add 10 Intruder Nodes with "midpoint_waypoiny" mobility
    (Every nodes with s9_connectivity)
    """
    project = 'sample9'

    Main.init(project)

    Static.metrics_model_filtered_path = f'{SimulationConfig.PROJECTS_DIR}{project}/MetricsModel-filtered-nc1.csv'

    for node in simulation.nodes():
        connectivity_model = cast(type['S9Connectivity'], ModelsSearchEngine.find_connectivity_model(
            f'{project}:s9_connectivity'))({})
        node.set_connectivity_model(connectivity_model)

    num_nodes = 10

    distribution_model_parameters: CircularDistParameters = {
        'number_of_nodes': num_nodes,
        'midpoint': [432000, 6475000],
        'rotation_direction': 'anti-clockwise',
        'radius': 1000
    }

    mobility_model_parameters: MidpointWaypointParameters = {
        'speed_range': [5, 13],
        'waiting_time_range': [50, 500],
        'waypoint_radius_range': [50, 500]
    }

    simulation.add_nodes(
        num_nodes=num_nodes,
        distribution_model_arg='circular_dist',
        node_arg=f'{project}:intruder_node',
        mobility_model_arg=f'{project}:midpoint_waypoint',
        connectivity_model_arg=f'{project}:s9_connectivity',
        interference_model_arg='no_interference',
        reliability_model_arg='reliable_delivery',
        node_color='#000000',
        node_size=3,
        distribution_model_parameters=distribution_model_parameters,
        mobility_model_parameters=mobility_model_parameters
    )

    Global.tracefile_suffix = '-nc1'

    return JsonResponse({"status": "success", "message": "OK", "project": project})


def network_configuration2(request):
    """
    Initialize project sample9
    Add 10 Intruder Nodes with "midpoint_waypoiny" mobility
    Add 15 Intruder Nodes with "mid_point_of_others" mobility
    (Every nodes with s9_connectivity)
    """
    project = 'sample9'

    Main.init(project)

    Static.metrics_model_filtered_path = f'{SimulationConfig.PROJECTS_DIR}{project}/MetricsModel-filtered-nc2.csv'

    for node in simulation.nodes():
        connectivity_model = cast(type['S9Connectivity'], ModelsSearchEngine.find_connectivity_model(
            f'{project}:s9_connectivity'))({})
        node.set_connectivity_model(connectivity_model)

    num_nodes = 10

    distribution_model_parameters: CircularDistParameters = {
        'number_of_nodes': num_nodes,
        'midpoint': [432000, 6475000],
        'rotation_direction': 'anti-clockwise',
        'radius': 1000
    }

    mobility_model_parameters_1: MidpointWaypointParameters = {
        'speed_range': [5, 13],
        'waiting_time_range': [50, 500],
        'waypoint_radius_range': [0, 200]
    }

    simulation.add_nodes(
        num_nodes=num_nodes,
        distribution_model_arg='circular_dist',
        node_arg=f'{project}:intruder_node',
        mobility_model_arg=f'{project}:midpoint_waypoint',
        connectivity_model_arg=f'{project}:s9_connectivity',
        interference_model_arg='no_interference',
        reliability_model_arg='reliable_delivery',
        node_color='#000000',
        node_size=3,
        distribution_model_parameters=distribution_model_parameters,
        mobility_model_parameters=mobility_model_parameters_1
    )

    num_nodes = 15

    distribution_model_parameters = {
        'number_of_nodes': num_nodes,
        'midpoint': [436000, 6472000],
        'rotation_direction': 'anti-clockwise',
        'radius': 500
    }

    mobility_model_parameters_2: MidPointOfOthersParameters = {
        'waypoint_radius_range': [0, 200]
    }

    simulation.add_nodes(
        num_nodes=num_nodes,
        distribution_model_arg='circular_dist',
        node_arg=f'{project}:intruder_node',
        mobility_model_arg=f'{project}:mid_point_of_others',
        connectivity_model_arg=f'{project}:s9_connectivity',
        interference_model_arg='no_interference',
        reliability_model_arg='reliable_delivery',
        node_color='#000033',
        node_size=3,
        distribution_model_parameters=distribution_model_parameters,
        mobility_model_parameters=mobility_model_parameters_2
    )

    Global.tracefile_suffix = '-nc2'

    return JsonResponse({"status": "success", "message": "OK", "project": project})


def network_configuration3(request):
    """
    Initialize project sample9
    Add 10 Intruder Nodes with "midpoint_waypoiny" mobility
    Add 15 Intruder Nodes with "mid_point_of_others" mobility
    Add 25 Intruder Nodes with "random_walk" mobility
    (Every nodes with s9_connectivity model)
    """
    project = 'sample9'

    Main.init(project)

    Static.metrics_model_filtered_path = f'{SimulationConfig.PROJECTS_DIR}{project}/MetricsModel-filtered-nc3.csv'

    for node in simulation.nodes():
        connectivity_model = ModelsSearchEngine.find_connectivity_model(
            f'{project}:s9_connectivity')({})
        node.set_connectivity_model(connectivity_model)

    num_nodes = 10

    mobility_model_parameters_1: MidpointWaypointParameters = {
        'speed_range': [5, 13],
        'waiting_time_range': [50, 500],
        'waypoint_radius_range': [0, 200]
    }

    distribution_model_parameters_1: CircularDistParameters = {
        'number_of_nodes': num_nodes,
        'midpoint': [432000, 6475000],
        'rotation_direction': 'anti-clockwise',
        'radius': 1000
    }

    simulation.add_nodes(
        num_nodes=num_nodes,
        distribution_model_arg='circular_dist',
        node_arg=f'{project}:intruder_node',
        mobility_model_arg=f'{project}:midpoint_waypoint',
        connectivity_model_arg=f'{project}:s9_connectivity',
        interference_model_arg='no_interference',
        reliability_model_arg='reliable_delivery',
        node_color='#000000',
        node_size=3,
        mobility_model_parameters=mobility_model_parameters_1,
        distribution_model_parameters=distribution_model_parameters_1
    )

    num_nodes = 15

    mobility_model_parameters_2: MidPointOfOthersParameters = {
        'waypoint_radius_range': [0, 200]
    }

    distribution_model_parameters_2: CircularDistParameters = {
        'number_of_nodes': num_nodes,
        'midpoint': [436000, 6472000],
        'rotation_direction': 'anti-clockwise',
        'radius': 500
    }

    simulation.add_nodes(
        num_nodes=num_nodes,
        distribution_model_arg='circular_dist',
        node_arg=f'{project}:intruder_node',
        mobility_model_arg=f'{project}:mid_point_of_others',
        connectivity_model_arg=f'{project}:s9_connectivity',
        interference_model_arg='no_interference',
        reliability_model_arg='reliable_delivery',
        node_color='#000033',
        node_size=3,
        distribution_model_parameters=distribution_model_parameters_2,
        mobility_model_parameters=mobility_model_parameters_2
    )

    num_nodes = 25

    distribution_model_parameters_3: CircularDistParameters = {
        'number_of_nodes': num_nodes,
        'midpoint': [434000, 6478000],
        'rotation_direction': 'anti-clockwise',
        'radius': 50
    }

    mobility_model_parameters_3: RandomWalkParameters = {
        'speed_range': [4, 12],
        'direction_range': [pi, 2 * pi],
        'prioritize_speed': False,
        'travel_distance': None,
        'travel_time': 50,
    }

    simulation.add_nodes(
        num_nodes=num_nodes,
        distribution_model_arg='circular_dist',
        node_arg=f'{project}:intruder_node',
        mobility_model_arg='random_walk',
        connectivity_model_arg=f'{project}:s9_connectivity',
        interference_model_arg='no_interference',
        reliability_model_arg='reliable_delivery',
        node_color='#003300',
        node_size=3,
        distribution_model_parameters=distribution_model_parameters_3,
        mobility_model_parameters=mobility_model_parameters_3
    )

    Global.tracefile_suffix = '-nc3'

    return JsonResponse({"status": "success", "message": "OK", "project": project})


def network_configuration4(request):
    """
    Initialize project sample9
    Add 100 Intruder Nodes with "random_walk" mobility
    (Every nodes with s9_connectivity)
    """
    project = 'sample9'

    Main.init(project)

    Static.metrics_model_filtered_path = f'{SimulationConfig.PROJECTS_DIR}{project}/MetricsModel-filtered-nc4.csv'

    for node in simulation.nodes():
        connectivity_model = ModelsSearchEngine.find_connectivity_model(
            f'{project}:s9_connectivity')({})
        node.set_connectivity_model(connectivity_model)

    num_nodes = 100

    mobility_model_parameters: RandomWalkParameters = {
        'speed_range': [4, 10],
        'direction_range': [pi, 2 * pi],
        'prioritize_speed': False,
        'travel_distance': None,
        'travel_time': 50,
    }

    distribution_model_parameters: CircularDistParameters = {
        'number_of_nodes': num_nodes,
        'midpoint': [434000, 6478000],
        'rotation_direction': 'anti-clockwise',
        'radius': 0
    }

    simulation.add_nodes(
        num_nodes=num_nodes,
        distribution_model_arg='circular_dist',
        node_arg=f'{project}:intruder_node',
        mobility_model_arg='random_walk',
        connectivity_model_arg=f'{project}:s9_connectivity',
        interference_model_arg='no_interference',
        reliability_model_arg='reliable_delivery',
        node_color='#003300',
        node_size=3,
        distribution_model_parameters=distribution_model_parameters,
        mobility_model_parameters=mobility_model_parameters
    )

    SimulationConfig.set_connectivity_enabled(True)

    Global.tracefile_suffix = '-nc4'

    return JsonResponse({"status": "success", "message": "OK", "project": project})


def network_configuration5(request):
    """
    Initialize project sample9
    Add 150 Intruder Nodes with "midpoint_waypoiny" mobility
    (Every nodes with s9_connectivity)
    """
    project = 'sample9'

    Main.init(project)

    Static.metrics_model_filtered_path = f'{SimulationConfig.PROJECTS_DIR}{project}/MetricsModel-filtered-nc5.csv'

    for node in simulation.nodes():
        connectivity_model = ModelsSearchEngine.find_connectivity_model(
            f'{project}:s9_connectivity')({})
        node.set_connectivity_model(connectivity_model)

    num_nodes = 150

    mobility_model_parameters: MidpointWaypointParameters = {
        'speed_range': [5, 13],
        'waiting_time_range': [50, 500],
        'waypoint_radius_range': [50, 500]
    }

    distribution_model_parameters: CircularDistParameters = {
        'number_of_nodes': num_nodes,
        'midpoint': [432000, 6475000],
        'rotation_direction': 'anti-clockwise',
        'radius': 1000
    }

    simulation.add_nodes(
        num_nodes=num_nodes,
        distribution_model_arg='circular_dist',
        node_arg=f'{project}:intruder_node',
        mobility_model_arg=f'{project}:midpoint_waypoint',
        connectivity_model_arg=f'{project}:s9_connectivity',
        interference_model_arg='no_interference',
        reliability_model_arg='reliable_delivery',
        node_color='#000000',
        node_size=3,
        mobility_model_parameters=mobility_model_parameters,
        distribution_model_parameters=distribution_model_parameters
    )

    Global.tracefile_suffix = '-nc5'

    return JsonResponse({"status": "success", "message": "OK", "project": project})


def network_configuration6(request):
    # Implement your network configuration 6 function here
    return JsonResponse({"status": "success", "message": "Not Implemented"})


def network_configuration7(request):
    # Implement your network configuration 7 function here
    return JsonResponse({"status": "success", "message": "Not Implemented"})


def network_configuration8(request):
    # Implement your network configuration 8 function here
    return JsonResponse({"status": "success", "message": "Not Implemented"})


def network_configuration9(request):
    # Implement your network configuration 9 function here
    return JsonResponse({"status": "success", "message": "Not Implemented"})


def network_configuration10(request):
    # Implement your network configuration 10 function here
    return JsonResponse({"status": "success", "message": "Not Implemented"})
