from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from .simulator.network_simulator import simulation
import json
from networkx.readwrite import json_graph
from .simulator.global_vars import Global
import os
from django.views.decorators.csrf import csrf_exempt
from .simulator.main import Main
from .simulator.tools.network_algorithms import NetworkAlgorithms
import networkx as nx
from .simulator.models.nodes.abc_node import AbcNode
from node2vec import Node2Vec
import numpy as np
import gensim
from copy import deepcopy

# Create your views here.
# Caminho para a pasta PROJECTS
PROJECTS_DIR = "apps/mobsinet/simulator/projects/"


def index(request):
    return render(request, "mobsinet_index.html")


def graph_view(request):
    return render(request, 'graph.html', {"projects": os.listdir(PROJECTS_DIR)})


def update_graph(request):

    node_link_data = json_graph.node_link_data(simulation.graph, edges="edges")

    nodes = list(map(lambda node: [node['id'].id, round(node['id'].position.x, 2), round(
        node['id'].position.y, 2), round(node['id'].position.z, 2), node['id'].size, node['id'].node_color.get_hex()], node_link_data.get('nodes')))
    links = []

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
        'logs': Global.round_logs,
        # 'algorithms': convert_keys_to_strings(NetworkAlgorithms.round_algorithms())
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
    return JsonResponse(os.listdir(PROJECTS_DIR), safe=False)


def init_simulation(request):
    project = request.GET.get('project')

    Main.init(project)

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
def update_config(request):
    if request.method == "POST":
        try:
            # Carrega os dados enviados no formulário
            form_data = request.POST.dict()

            # Carrega o JSON existente
            with open(os.path.join(PROJECTS_DIR, form_data['project'], 'config.json'), "r") as json_file:
                existing_data = json.load(json_file)

            # Atualiza os dados existentes com os dados do formulário
            updated_data = merge_data(existing_data, form_data)

            # Salva o JSON atualizado no arquivo
            with open(os.path.join(PROJECTS_DIR, form_data['project'], 'config.json'), "w") as json_file:
                json.dump(updated_data, json_file, indent=4)

            # Retorna uma resposta de sucesso
            return JsonResponse({"status": "success", "message": "JSON atualizado com sucesso!"})
        except Exception as e:
            # Retorna uma resposta de erro
            print(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse("Método não permitido", status=405)


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
        with open(os.path.join(PROJECTS_DIR, request.GET.get('project'), 'config.json'), "r") as json_file:
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
        degree: int = simulation.graph.degree(node)

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
        simulation.graph, dimensions=int(dimensions), workers=4)

    # For compatibility with the project version of gensim
    node2vec.fit = new_fit_for_node2vec

    model = node2vec.fit(node2vec, window=10, min_count=1, batch_words=4)

    # Obtém os nós e os vetores
    words = list(model.wv.index_to_key)  # Lista de nós
    vectors = np.array([model.wv[word]
                       for word in words])  # Vetores (já em 2D)

    return JsonResponse({"words": words, "vectors": vectors.tolist()})


def add_nodes(request):
    if request.method == "POST":

        from .simulator.configuration.sim_config import config
        # Carrega os dados enviados no formulário
        form_data = parse_nested_dict(request.POST.dict())

        print(form_data)

        original_config = deepcopy(config)

        config.set_node(form_data['node'])
        config.set_distribution_model(form_data['distribution_model'])
        config.set_mobility_model(form_data['mobility_model'])
        config.set_connectivity_model(form_data['connectivity_model'])
        config.set_interference_model(form_data['interference_model'])
        config.set_reliability_model(form_data['reliability_model'])
        config.set_distribution_model_parameters(
            form_data['distribution_model_parameters'] if 'distribution_model_parameters' in form_data else None)
        config.set_mobility_model_parameters(
            form_data['mobility_model_parameters'] if 'mobility_model_parameters' in form_data else None)
        config.set_connectivity_model_parameters(
            form_data['connectivity_model_parameters'] if 'connectivity_model_parameters' in form_data else None)
        config.set_interference_model_parameters(
            form_data['interference_model_parameters'] if 'interference_model_parameters' in form_data else None)
        config.set_reliability_model_parameters(
            form_data['reliability_model_parameters'] if 'reliability_model_parameters' in form_data else None)

        simulation.add_nodes(
            num_nodes=int(form_data['num_nodes']),
            distribution_model=config.distribution_model,
            node_constructor=config.node,
            mobility_model=config.mobility_model,
            connectivity_model=config.connectivity_model,
            interference_model=config.interference_model,
            reliability_model=config.reliability_model,
        )

        config = original_config

        # Retorna uma resposta de sucesso
        return JsonResponse({"status": "success", "message": "JSON atualizado com sucesso!"})

    else:
        return HttpResponse("Método não permitido", status=405)


def parse_nested_dict(flat_dict):
    nested_dict = {}

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
