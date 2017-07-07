#
import pytest
import numpy as np

class TestGlobal(object):

    # inputs

    def test_model_size(self, g_fixture):
        assert g_fixture.econ.size == g_fixture.industry_count

    def test_use_table(self, g_fixture):
        assert len(g_fixture.econ.use_table) == g_fixture.commodity_count
        assert len(g_fixture.econ.use_table[0]) == g_fixture.industry_count

    def test_make_table(self, g_fixture):
        assert len(g_fixture.econ.make_table) == g_fixture.industry_count
        assert len(g_fixture.econ.make_table[0]) == g_fixture.commodity_count

    def test_industry_vector(self, g_fixture):
        assert len(g_fixture.econ.industry_vector) == g_fixture.industry_count

    def test_commodity_vector(self, g_fixture):
        assert len(g_fixture.econ.commodity_vector) == g_fixture.commodity_count

    def test_value_vector(self, g_fixture):
        assert len(g_fixture.econ.value_vector) == g_fixture.industry_count

    def test_noncomp_vector(self, g_fixture):
        assert len(g_fixture.econ.noncomp_vector) == g_fixture.industry_count

    def test_demand_vector(self, g_fixture):
        assert len(g_fixture.econ.demand_vector) == g_fixture.commodity_count
        assert len(g_fixture.econ.demand_vector[0]) == 1

    def test_identity(self, g_fixture):
        assert len(g_fixture.econ.identity) == g_fixture.commodity_count
        assert len(g_fixture.econ.identity[0]) == g_fixture.commodity_count

    def test_industry_legend(self, g_fixture):
        assert len(g_fixture.econ.industry_legend) == g_fixture.industry_count
        if g_fixture.industry_count == 15:
            assert g_fixture.econ.industry_legend[0] == 'Agriculture, forestry, fishing, and hunting'
        elif g_fixture.industry_count == 71:
            assert g_fixture.econ.industry_legend[0] == 'Farms'

    def test_commodity_legend(self, g_fixture):
        assert len(g_fixture.econ.commodity_legend) == g_fixture.commodity_count
        if g_fixture.commodity_count == 17:
            assert g_fixture.econ.commodity_legend[0] == 'Agriculture, forestry, fishing, and hunting'
        elif g_fixture.commodity_count == 73:
            assert g_fixture.econ.commodity_legend[0] == 'Farms'
        penult_idx = g_fixture.commodity_count - 2
        last_idx = g_fixture.commodity_count - 1
        assert g_fixture.econ.commodity_legend[penult_idx] == 'Scrap, used and secondhand goods'
        assert g_fixture.econ.commodity_legend[last_idx] == 'Noncomparable imports and rest-of-the-world adjustment [1]'

    def test_cxi_null_matrix(self, g_fixture):
        assert len(g_fixture.econ.cxi_null_matrix) == g_fixture.commodity_count
        assert len(g_fixture.econ.cxi_null_matrix[0]) == g_fixture.industry_count
        expected = np.zeros((g_fixture.commodity_count, g_fixture.industry_count))
        np.testing.assert_array_equal(g_fixture.econ.cxi_null_matrix, expected)

    # balancing derivations

    def test_direct_req(self, g_fixture):
        assert len(g_fixture.econ.direct_req) == g_fixture.commodity_count
        np.testing.assert_almost_equal(g_fixture.econ.direct_req,
                                       g_fixture.test_derivations.direct_req_matrix,
                                       decimal=4)

    def test_market_share(self, g_fixture):
        assert len(g_fixture.econ.market_share) == g_fixture.industry_count
        np.testing.assert_almost_equal(g_fixture.econ.market_share,
                                       g_fixture.test_derivations.market_share_matrix,
                                       decimal=5)

    def test_tech_coefficient(self, g_fixture):
        assert len(g_fixture.econ.tech_coefficient) == g_fixture.commodity_count
        expected = np.dot(g_fixture.test_derivations.direct_req_matrix,
                          g_fixture.test_derivations.market_share_matrix)
        np.testing.assert_almost_equal(g_fixture.econ.tech_coefficient,
                                       expected,
                                       decimal=4)

    def test_leontief_inverse(self, g_fixture):
        assert len(g_fixture.econ.leontief_inverse) == g_fixture.commodity_count
        assert len(g_fixture.econ.leontief_inverse[0]) == g_fixture.commodity_count
        np.testing.assert_almost_equal(g_fixture.econ.leontief_inverse,
                                       g_fixture.test_derivations.total_req_matrix,
                                       decimal=4)

    def test_total_requirements(self, g_fixture):
        assert len(g_fixture.econ.total_requirements) == g_fixture.commodity_count
        expected = np.dot(g_fixture.test_derivations.total_req_matrix,
                          g_fixture.econ.demand_vector)
        np.testing.assert_allclose(g_fixture.econ.total_requirements,
                                   expected,
                                   rtol=1e-2, atol=0)

    def test_unit_requirements(self, g_fixture):
        assert len(g_fixture.econ.unit_requirements) == g_fixture.commodity_count
        np.testing.assert_almost_equal(g_fixture.econ.unit_requirements,
                                       g_fixture.test_derivations.output_req_vector,
                                       decimal=3)

    def test_unit_price(self, g_fixture):
        assert len(g_fixture.econ.unit_price) == g_fixture.commodity_count
        np.testing.assert_almost_equal(g_fixture.econ.unit_price,
                                       np.ones(g_fixture.commodity_count),
                                       decimal=1)

    # modeling derivations

    def test_tax_matrix(self, g_fixture):
        mock_args = g_fixture.econ.model_args
        expected = np.zeros((g_fixture.commodity_count, g_fixture.industry_count))
        for arg in mock_args:
            commodity, rate = arg
            expected[commodity].fill(rate)
        np.testing.assert_array_equal(g_fixture.econ.tax_matrix, expected)

    def test_tax_coefficient(self, g_fixture):
        assert len(g_fixture.econ.tax_coefficient) == g_fixture.commodity_count

    def test_rel_coefficient(self, g_fixture):
        expected = np.subtract(g_fixture.econ.rel_coefficient,
                                        g_fixture.econ.tax_coefficient)[0]
        assert len(g_fixture.econ.tax_coefficient) == g_fixture.commodity_count
        np.testing.assert_almost_equal(g_fixture.econ.value_coefficient,
                                       expected, decimal=1)

    def test_rel_unit_price(self, g_fixture):
        rel_unit_price = g_fixture.econ.rel_unit_price
        rel_coefficient = np.linalg.lstsq(g_fixture.econ.leontief_inverse_trans, rel_unit_price)[0]
        value_coefficient = np.subtract(rel_coefficient, g_fixture.econ.tax_coefficient)[0]
        asserted = np.dot(g_fixture.econ.leontief_inverse_trans, value_coefficient)[0]
        expected = np.ones(g_fixture.commodity_count)
        assert len(rel_unit_price) == g_fixture.commodity_count
        np.testing.assert_almost_equal(asserted, expected, decimal=1)

    # helper methods

    def test_get_x(self, g_fixture):
        if g_fixture.industry_count == 15:
            assert g_fixture.econ.get_x('Agriculture, forestry, fishing, and hunting') == 0
        elif g_fixture.industry_count == 71:
            assert g_fixture.econ.get_x('Farms') == 0

    def test_get_y(self, g_fixture):
        if g_fixture.commodity_count == 17:
            assert g_fixture.econ.get_y('Agriculture, forestry, fishing, and hunting') == 0
        elif g_fixture.commodity_count == 73:
            assert g_fixture.econ.get_y('Farms') == 0
        penult_item = 'Scrap, used and secondhand goods'
        last_item = 'Noncomparable imports and rest-of-the-world adjustment [1]'
        assert g_fixture.econ.get_y(last_item) == g_fixture.commodity_count - 1
        assert g_fixture.econ.get_y(penult_item) == g_fixture.commodity_count - 2
#
