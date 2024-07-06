from django.shortcuts import render
from rest_framework.views import APIView, View
from rest_framework.request import Request
from .query_parsers.RandomWalk import RandomWalkQueryParser
from .inspectors.RandomWalk import RandomWalkQueryDataInspector
from .generator.simulations.RandomWalkSimulation import RandomWalkSimulation
from django.http import StreamingHttpResponse

# Create your views here.
class HomeView(APIView):
    def get(self, request: Request):
        return render(request, "mobgen_index.html")

class RandomWalkView(View):
    def get(self, request: Request):
        return render(request, "random_walk.html")

class RandomWalkStreamingView(APIView):
    def get(self, request: Request):
        
        query = RandomWalkQueryParser(request.query_params).get_query()
        queryData = RandomWalkQueryDataInspector(query).get_query_data()
        simulation = RandomWalkSimulation(queryData)

        return StreamingHttpResponse(simulation.start())

        

