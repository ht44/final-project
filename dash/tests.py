from django.test import TestCase
from django.test import Client
from iomodel import model as m
import numpy as np

client = Client()

class DashApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.econ = m.Leontief('sector', '2015', sql=True)

    def test_dash_index_resp_sector_mostrec_year(self):
        response = client.get('/dash/')
        parsed = response.json()
        self.assertEqual(parsed['level'], 'sector')
        self.assertEqual(parsed['year'], 2015)
        self.assertIn('use_matrix', parsed)
        self.assertIn('make_matrix', parsed)
        self.assertIn('industry_vector', parsed)
        self.assertIn('commodity_vector', parsed)
        self.assertIn('value_vector', parsed)
        self.assertIn('demand_vector', parsed)
        self.assertIn('noncomp_vector', parsed)
        self.assertEqual(parsed['use_matrix'], self.econ.use_matrix.tolist())
        self.assertEqual(parsed['make_matrix'], self.econ.make_matrix.tolist())
        self.assertEqual(parsed['industry_vector'], self.econ.industry_vector.tolist())
        self.assertEqual(parsed['commodity_vector'], self.econ.commodity_vector.tolist())
        self.assertEqual(parsed['value_vector'], self.econ.value_vector.tolist())
        self.assertEqual(parsed['demand_vector'], self.econ.demand_vector.tolist())
        self.assertEqual(parsed['noncomp_vector'], self.econ.noncomp_vector.tolist())
