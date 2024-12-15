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
        node['id'].position.y, 2)], node_link_data.get('nodes')))
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
    }

    return JsonResponse(graph_data)


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
        simulation.running_thread.stop()

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
