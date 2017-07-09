#
import os
import pytest
import pandas as pd
import random
from .. import model
from .. import data
Leontief = model.Leontief
Dataset = data.Dataset

def pytest_addoption(parser):
    parser.addoption('--year', action='store', default='2015')

class Taggable(object):
    pass

class ModelFixture:
    def __init__(self, level, year):

        self.level = level
        self.year = year
        self.industry_count = None
        self.commodity_count = None
        self.test_derivations = Taggable()
        self.test_derivations.demand_vector = pd.read_pickle(
            os.path.join('model/pickles', self.level, self.year, 'demand.pkl')).as_matrix().astype('float')
        self.test_derivations.market_share_matrix = pd.read_pickle(
            os.path.join('model/test/bea_derivations', self.level, self.year, 'market.pkl')).as_matrix().astype('float')
        self.test_derivations.direct_req_matrix = pd.read_pickle(
            os.path.join('model/test/bea_derivations', self.level, self.year, 'direct.pkl')).as_matrix().astype('float')
        self.test_derivations.total_req_matrix = pd.read_pickle(
            os.path.join('model/test/bea_derivations', self.level, self.year, 'total.pkl')).as_matrix().astype('float')
        self.test_derivations.output_req_vector = pd.read_pickle(
            os.path.join('model/test/bea_derivations', self.level, self.year, 'output.pkl')).as_matrix()[0].astype('float')

        if level == 'sector':
            self.test_derivations.industry_count = 15
            self.test_derivations.commodity_count = 17
        elif self.level == 'summary':
            self.test_derivations.industry_count = 71
            self.test_derivations.commodity_count = 73

        self.econ = Leontief(self.level, self.year)

    def gen_random_model(self):

        rand_comms = random.sample(range(self.test_derivations.commodity_count), 6)
        rand_rates = [random.random() for i in range(6)]
        rand_deltas = random.sample(range(1, 1000), 6)
        for i in range(0, len(rand_deltas), 2):
            rand_deltas[i] = rand_deltas[i] * -1
        rand_price_args = zip(rand_comms, rand_rates)
        rand_demand_args = zip(rand_comms, rand_deltas)

        self.econ.balance()
        self.econ.model_price(list(rand_price_args))
        self.econ.model_output(list(rand_demand_args))

@pytest.fixture(scope='class', params=['sector', 'summary'])
def single_year(request):
    level = request.param
    year = request.config.getoption('year')
    fixture = ModelFixture(level, year)
    fixture.gen_random_model()
    yield fixture
    fixture = None

@pytest.fixture(scope='class', params=[
    ('sector', '1997'), ('sector', '1998'), ('sector', '1999'),
    ('sector', '2000'), ('sector', '2001'), ('sector', '2002'),
    ('sector', '2003'), ('sector', '2004'), ('sector', '2005'),
    ('sector', '2006'), ('sector', '2007'), ('sector', '2008'),
    ('sector', '2009'), ('sector', '2010'), ('sector', '2011'),
    ('sector', '2012'), ('sector', '2013'), ('sector', '2014'), ('sector', '2015'),
    ('summary', '1997'), ('summary', '1998'), ('summary', '1999'),
    ('summary', '2000'), ('summary', '2001'), ('summary', '2002'),
    ('summary', '2003'), ('summary', '2004'), ('summary', '2005'),
    ('summary', '2006'), ('summary', '2007'), ('summary', '2008'),
    ('summary', '2009'), ('summary', '2010'), ('summary', '2011'),
    ('summary', '2012'), ('summary', '2013'), ('summary', '2014'), ('summary', '2015')
], ids=[
    'sect97', 'sect98', 'sect99', 'sect00', 'sect01', 'sect02', 'sect03',
    'sect04', 'sect05', 'sect06', 'sect07', 'sect08', 'sect09', 'sect10',
    'sect11', 'sect12', 'sect13', 'sect14', 'sect15',
    'summ97', 'summ98', 'summ99', 'summ00', 'summ01', 'summ02', 'summ03',
    'summ04', 'summ05', 'summ06', 'summ07', 'summ08', 'summ09', 'summ10',
    'summ11', 'summ12', 'summ13', 'summ14', 'summ15'])
def multi_year(request):
    level, year = request.param
    fixture = ModelFixture(level, year)
    fixture.gen_random_model()
    yield fixture
    fixture = None
#
