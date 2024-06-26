from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from . import net

# Create your views here.
def index(request):
    return render(request, "mobsinet_index.html")


def graph_view(request):

    graph_div = net.graph_view(request)

    return render(request, 'graph.html', {'graph_div': graph_div})


def update_graph(request):

    graph_div = net.update_graph()

    return JsonResponse({'graph_div': graph_div})