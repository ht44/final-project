#
import os
import pytest
import pandas as pd
from copy import deepcopy
from ... import model
from ... import data

Leontief = model.Leontief
Dataset = data.Dataset

def pytest_addoption(parser):
    parser.addoption('--year', action='store', default='2015')

@pytest.fixture(scope='class', params=['sector', 'summary'])
def fixture(request):
    class ModelFixture:
        def __init__(self, level, year):
            self.level = level
            self.year = year
            self.industry_count = None
            self.commodity_count = None
            self.test_derivations = None

        def get_industry_count(self):
            industry_count = None
            if self.level == 'sector':
                industry_count = 15
            elif self.level == 'summary':
                industry_count = 71
            return industry_count

        def get_commodity_count(self):
            commodity_count = None
            if self.level == 'sector':
                commodity_count = 17
            elif self.level == 'summary':
                commodity_count = 73
            return commodity_count

        def get_test_derivations(self):
            class Deriv(object):
                pass
            td = Deriv()
            td.market_share_matrix = pd.read_pickle(
                os.path.join('app/test/bea_derivations', self.level, self.year, 'market.pkl')).as_matrix().astype('float')
            td.direct_req_matrix = pd.read_pickle(
                os.path.join('app/test/bea_derivations', self.level, self.year, 'direct.pkl')).as_matrix().astype('float')
            td.total_req_matrix = pd.read_pickle(
                os.path.join('app/test/bea_derivations', self.level, self.year, 'total.pkl')).as_matrix().astype('float')
            td.output_req_vector = pd.read_pickle(
                os.path.join('app/test/bea_derivations', self.level, self.year, 'output.pkl')).as_matrix()[0].astype('float')
            return td

        def get_econ(self):
            data = Dataset(self.level, self.year)
            econ = Leontief(data)
            econ.balance()
            return econ

        def fix(self):
            self.industry_count = self.get_industry_count()
            self.commodity_count = self.get_commodity_count()
            self.test_derivations = self.get_test_derivations()
            self.econ = self.get_econ()



    fixture = ModelFixture(request.param, request.config.getoption('--year'))
    fixture.fix()
    yield fixture
    fixture = None
#
