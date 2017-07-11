from django.test import TestCase
from django.test import Client

client = Client()

class DashApiTest(TestCase):
    def test_dash_index_resp_sector_mostrec_year(self):
        response = client.get('/dash/')
        parsed = response.json()
        self.assertEqual(parsed.level, 'sector')
        self.assertEqual(parsed.year, '2015')

# Create your tests here.
