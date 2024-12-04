from django.shortcuts import render
# Create your views here.


def home(request):

    data = {"content": "test"}
    return render(request, "home.html", data)