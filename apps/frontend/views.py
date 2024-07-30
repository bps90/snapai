from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.


def home(request):

    data = {"content": "test"}
    return render(request, "home.html", data)