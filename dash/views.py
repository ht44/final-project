from django.shortcuts import render
from django.http import HttpResponse
from iomodel import model as m
import json

def index(request):
    econ = m.Leontief('sector', '2015', sql=True)
    resp = {
        'level': 'sector',
        'year': 2015,
        'use_matrix': econ.use_matrix.tolist(),
        'make_matrix': econ.make_matrix.tolist(),
        'industry_vector': econ.industry_vector.tolist(),
        'commodity_vector': econ.commodity_vector.tolist(),
        'value_vector': econ.value_vector.tolist(),
        'demand_vector': econ.demand_vector.tolist(),
        'noncomp_vector': econ.noncomp_vector.tolist()}
    return HttpResponse(json.dumps(resp), content_type='application/json')

def filter(request, level, year):
    econ = m.Leontief(level, year, sql=True)
    resp = {
        'level': level,
        'year': int(year),
        'use_matrix': econ.use_matrix.tolist(),
        'make_matrix': econ.make_matrix.tolist(),
        'industry_vector': econ.industry_vector.tolist(),
        'commodity_vector': econ.commodity_vector.tolist(),
        'value_vector': econ.value_vector.tolist(),
        'demand_vector': econ.demand_vector.tolist(),
        'noncomp_vector': econ.noncomp_vector.tolist()}
    return HttpResponse(json.dumps(resp), content_type='application/json')
