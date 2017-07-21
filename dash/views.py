import json
import decimal
import pandas as pd
from dash.models import *
from iomodel import model as mod
from django.http import HttpResponse
from django.shortcuts import render

Decimal = decimal.Decimal
decimal.getcontext().prec = 1

def dj_to_df(djmod, year):
    return pd.DataFrame(
        list(
            djmod.objects.filter(year=year).values()
        )
    ).pivot(index='row', columns='col', values='val')

def index(request):

    u = dj_to_df(SectorUse, '2015')
    m = dj_to_df(SectorMake, '2015')
    i = dj_to_df(SectorIndustry, '2015')
    c = dj_to_df(SectorCommodity, '2015')
    v = dj_to_df(SectorValue, '2015')
    d = dj_to_df(SectorDemand, '2015')
    n = dj_to_df(SectorNoncomp, '2015')

    econ = m.Leontief(u, m, i, c, v, d, n)
    econ.balance()

    resp = {
        'level': 'sector',
        'year': 2015,
        'unit_price': econ.unit_price.tolist(),
        'legend': [rec.name for rec in Legend.objects.filter(level='sector')]
    }

    return HttpResponse(json.dumps(resp), content_type='application/json')

def filter(request, level, year):

    def is_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    if level == 'sector':

        u = dj_to_df(SectorUse, year)
        m = dj_to_df(SectorMake, year)
        i = dj_to_df(SectorIndustry, year)
        c = dj_to_df(SectorCommodity, year)
        v = dj_to_df(SectorValue, year)
        d = dj_to_df(SectorDemand, year)
        n = dj_to_df(SectorNoncomp, year)

    elif level == 'summary':

        u = dj_to_df(SummaryUse, year)
        m = dj_to_df(SummaryMake, year)
        i = dj_to_df(SummaryIndustry, year)
        c = dj_to_df(SummaryCommodity, year)
        v = dj_to_df(SummaryValue, year)
        d = dj_to_df(SummaryDemand, year)
        n = dj_to_df(SummaryNoncomp, year)

    econ = mod.Leontief(u, m, i, c, v, d, n)
    econ.balance()

    resp = {
        'level': level,
        'year': int(year),
        'unit_price': econ.unit_price.tolist(),
        'legend': [rec.name for rec in Legend.objects.filter(level=level)]
    }

    if request.GET.__contains__('arg'):

        args = request.GET.copy()
        args = [(int(a), float(b)) for a, b in args.items() if is_int(a)]
        econ.model_price(args)
        resp['rel_unit_price'] = econ.rel_unit_price.tolist()

    return HttpResponse(json.dumps(resp), content_type='application/json')
