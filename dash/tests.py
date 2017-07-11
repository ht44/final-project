from django.test import TestCase
from django.test import Client
from iomodel import model as m
import numpy as np

client = Client()

class DashApiIndexTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.econ = m.Leontief('sector', '2015', sql=True)
        cls.econ.balance()
        cls.response = client.get('/dash/')
        cls.parsed = cls.response.json()

    @classmethod
    def tearDownClass(cls):
        del cls

    def test_dash_index_resp(self):
        self.assertEqual(self.parsed['level'], 'sector')
        self.assertEqual(self.parsed['year'], 2015)
        self.assertEqual(self.parsed['use_matrix'], self.econ.use_matrix.tolist())
        self.assertEqual(self.parsed['make_matrix'], self.econ.make_matrix.tolist())
        self.assertEqual(self.parsed['industry_vector'], self.econ.industry_vector.tolist())
        self.assertEqual(self.parsed['commodity_vector'], self.econ.commodity_vector.tolist())
        self.assertEqual(self.parsed['value_vector'], self.econ.value_vector.tolist())
        self.assertEqual(self.parsed['demand_vector'], self.econ.demand_vector.tolist())
        self.assertEqual(self.parsed['noncomp_vector'], self.econ.noncomp_vector.tolist())
        self.assertEqual(self.parsed['direct_req'], self.econ.direct_req.tolist())
        self.assertEqual(self.parsed['market_share'], self.econ.market_share.tolist())
        self.assertEqual(self.parsed['leontief_inverse'], self.econ.leontief_inverse.tolist())
        self.assertEqual(self.parsed['total_requirements'], self.econ.total_requirements.tolist())
        self.assertEqual(self.parsed['unit_requirements'], self.econ.unit_requirements.tolist())
        self.assertEqual(self.parsed['unit_price'], self.econ.unit_price.tolist())

class DashApiFilterTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.level = 'sector'
        cls.year = 2015
        cls.econ = m.Leontief(cls.level, str(cls.year), sql=True)
        cls.econ.balance()
        cls.response = client.get(f'/dash/{cls.level}/{cls.year}/')
        cls.parsed = cls.response.json()

    @classmethod
    def tearDownClass(cls):
        del cls

    def test_dash_filter_resp(self):
        self.assertEqual(self.parsed['level'],
                         self.level)
        self.assertEqual(self.parsed['year'],
                         self.year)
        self.assertEqual(self.parsed['use_matrix'],
                         self.econ.use_matrix.tolist())
        self.assertEqual(self.parsed['make_matrix'],
                         self.econ.make_matrix.tolist())
        self.assertEqual(self.parsed['industry_vector'],
                         self.econ.industry_vector.tolist())
        self.assertEqual(self.parsed['commodity_vector'],
                         self.econ.commodity_vector.tolist())
        self.assertEqual(self.parsed['value_vector'],
                         self.econ.value_vector.tolist())
        self.assertEqual(self.parsed['demand_vector'],
                         self.econ.demand_vector.tolist())
        self.assertEqual(self.parsed['noncomp_vector'],
                         self.econ.noncomp_vector.tolist())
        self.assertEqual(self.parsed['direct_req'], self.econ.direct_req.tolist())
        self.assertEqual(self.parsed['market_share'], self.econ.market_share.tolist())
        self.assertEqual(self.parsed['leontief_inverse'], self.econ.leontief_inverse.tolist())
        self.assertEqual(self.parsed['total_requirements'], self.econ.total_requirements.tolist())
        self.assertEqual(self.parsed['unit_requirements'], self.econ.unit_requirements.tolist())
        self.assertEqual(self.parsed['unit_price'], self.econ.unit_price.tolist())
