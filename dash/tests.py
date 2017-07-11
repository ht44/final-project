from django.test import TestCase
from django.test import Client
from iomodel import model as m
import numpy as np

client = Client()

class DashApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.econ = m.Leontief('sector', '2015', sql=True)
        cls.response = client.get('/dash/')
        cls.parsed = cls.response.json()

    @classmethod
    def tearDownClass(cls):
        del cls.econ
        del cls.response
        del cls.parsed

    def test_dash_index_resp(self):
        self.assertEqual(self.parsed['level'], 'sector')
        self.assertEqual(self.parsed['year'], 2015)
        self.assertIn('use_matrix', self.parsed)
        self.assertIn('make_matrix', self.parsed)
        self.assertIn('industry_vector', self.parsed)
        self.assertIn('commodity_vector', self.parsed)
        self.assertIn('value_vector', self.parsed)
        self.assertIn('demand_vector', self.parsed)
        self.assertIn('noncomp_vector', self.parsed)
        self.assertEqual(self.parsed['use_matrix'], self.econ.use_matrix.tolist())
        self.assertEqual(self.parsed['make_matrix'], self.econ.make_matrix.tolist())
        self.assertEqual(self.parsed['industry_vector'], self.econ.industry_vector.tolist())
        self.assertEqual(self.parsed['commodity_vector'], self.econ.commodity_vector.tolist())
        self.assertEqual(self.parsed['value_vector'], self.econ.value_vector.tolist())
        self.assertEqual(self.parsed['demand_vector'], self.econ.demand_vector.tolist())
        self.assertEqual(self.parsed['noncomp_vector'], self.econ.noncomp_vector.tolist())
