from django.shortcuts import render
from django.http import HttpResponse
import json

def index(request):
    res = {
        'level': 'sector',
        'year': 2015,
        'use_matrix': '',
        'make_matrix': '',
        'industry_vector': '',
        'commodity_vector': '',
        'value_vector': '',
        'demand_vector': '',
        'noncomp_vector': '',
    }
    return HttpResponse(json.dumps(res), content_type='application/json')
