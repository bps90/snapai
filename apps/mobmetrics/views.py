from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

import pandas as pd

from .process.main import main

def index(request):
    return render(request, "mobmetrics_index.html")

def upload_file(request):
  ''' Recive .csv file'''
  if request.method == 'POST' and request.FILES.get('file'):
      file = request.FILES['file']
      
      main(file)

      return JsonResponse({'message': 'File uploaded successfully'})
  return JsonResponse({'message': 'Failed to upload file'}, status=400)
