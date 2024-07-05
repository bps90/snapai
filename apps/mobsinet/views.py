from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
#from .sim.net import graph

# Create your views here.
def index(request):

    return render(request, "mobsinet_index.html")


def graph_view(request):
    pass
    #graph_div = graph.graph_view(request)

    #return render(request, 'graph.html', {'graph_div': graph_div})


def update_graph(request):
    pass
    #graph_div = graph.update_graph()

    #return JsonResponse({'graph_div': graph_div})