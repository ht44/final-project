from django.shortcuts import render
from django.http import HttpResponse
import json

def index(request):
    res = {'level': 'sector', 'year': 2015}
    return HttpResponse(json.dumps(res), content_type='application/json')
