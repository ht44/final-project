from django.test import TestCase
from django.test import Client

client = Client()

class DashApiTest(TestCase):
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
