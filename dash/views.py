from django.shortcuts import render
from django.http import HttpResponse
from iomodel import model as m
import json

def index(request):
    econ = m.Leontief('sector', '2015', sql=True)
    econ.balance()
    resp = {
        'level': 'sector',
        'year': 2015,
        'use_matrix': econ.use_matrix.tolist(),
        'make_matrix': econ.make_matrix.tolist(),
        'industry_vector': econ.industry_vector.tolist(),
        'commodity_vector': econ.commodity_vector.tolist(),
        'value_vector': econ.value_vector.tolist(),
        'demand_vector': econ.demand_vector.tolist(),
        'noncomp_vector': econ.noncomp_vector.tolist(),
        'direct_req': econ.direct_req.tolist(),
        'market_share': econ.market_share.tolist(),
        'leontief_inverse': econ.leontief_inverse.tolist(),
        'total_requirements': econ.total_requirements.tolist(),
        'unit_requirements': econ.unit_requirements.tolist(),
        'unit_price': econ.unit_price.tolist(),
        }
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
