#
import os
import pytest
import pandas as pd
import numpy as np
import random
from copy import deepcopy
from ... import model
from ... import data

Leontief = model.Leontief
Dataset = data.Dataset

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
    'summ11', 'summ12', 'summ13', 'summ14', 'summ15'
])
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
            rand_comms = random.sample(range(self.commodity_count), 3)
            rand_rates = [random.random() for i in range(2)]
            mock_args = zip(rand_comms, rand_rates)
            data = Dataset(self.level, self.year)
            econ = Leontief(data)
            econ.balance()
            econ.model(list(mock_args))
            return econ

        def fix(self):
            self.industry_count = self.get_industry_count()
            self.commodity_count = self.get_commodity_count()
            self.test_derivations = self.get_test_derivations()
            self.econ = self.get_econ()

    level, year = request.param
    fixture = ModelFixture(level, year)
    fixture.fix()
    yield fixture
    fixture = None
#
