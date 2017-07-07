#
import pytest
import numpy as np

class TestModel(object):

    # inputs

    def test_model_size(self, y_fixture):
        assert y_fixture.econ.size == y_fixture.industry_count

    def test_use_table(self, y_fixture):
        assert len(y_fixture.econ.use_table) == y_fixture.commodity_count
        assert len(y_fixture.econ.use_table[0]) == y_fixture.industry_count

    def test_make_table(self, y_fixture):
        assert len(y_fixture.econ.make_table) == y_fixture.industry_count
        assert len(y_fixture.econ.make_table[0]) == y_fixture.commodity_count

    def test_industry_vector(self, y_fixture):
        assert len(y_fixture.econ.industry_vector) == y_fixture.industry_count

    def test_commodity_vector(self, y_fixture):
        assert len(y_fixture.econ.commodity_vector) == y_fixture.commodity_count

    def test_value_vector(self, y_fixture):
        assert len(y_fixture.econ.value_vector) == y_fixture.industry_count

    def test_noncomp_vector(self, y_fixture):
        assert len(y_fixture.econ.noncomp_vector) == y_fixture.industry_count

    def test_demand_vector(self, y_fixture):
        assert len(y_fixture.econ.demand_vector) == y_fixture.commodity_count
        assert len(y_fixture.econ.demand_vector[0]) == 1

    def test_identity(self, y_fixture):
        assert len(y_fixture.econ.identity) == y_fixture.commodity_count
        assert len(y_fixture.econ.identity[0]) == y_fixture.commodity_count

    def test_industry_legend(self, y_fixture):
        assert len(y_fixture.econ.industry_legend) == y_fixture.industry_count
        if y_fixture.industry_count == 15:
            assert y_fixture.econ.industry_legend[0] == 'Agriculture, forestry, fishing, and hunting'
        elif y_fixture.industry_count == 71:
            assert y_fixture.econ.industry_legend[0] == 'Farms'

    def test_commodity_legend(self, y_fixture):
        assert len(y_fixture.econ.commodity_legend) == y_fixture.commodity_count
        if y_fixture.commodity_count == 17:
            assert y_fixture.econ.commodity_legend[0] == 'Agriculture, forestry, fishing, and hunting'
        elif y_fixture.commodity_count == 73:
            assert y_fixture.econ.commodity_legend[0] == 'Farms'
        penult_idx = y_fixture.commodity_count - 2
        last_idx = y_fixture.commodity_count - 1
        assert y_fixture.econ.commodity_legend[penult_idx] == 'Scrap, used and secondhand goods'
        assert y_fixture.econ.commodity_legend[last_idx] == 'Noncomparable imports and rest-of-the-world adjustment [1]'

    def test_cxi_null_matrix(self, y_fixture):
        assert len(y_fixture.econ.cxi_null_matrix) == y_fixture.commodity_count
        assert len(y_fixture.econ.cxi_null_matrix[0]) == y_fixture.industry_count
        expected = np.zeros((y_fixture.commodity_count, y_fixture.industry_count))
        np.testing.assert_array_equal(y_fixture.econ.cxi_null_matrix, expected)

    # balancing derivations

    def test_direct_req(self, y_fixture):
        assert len(y_fixture.econ.direct_req) == y_fixture.commodity_count
        np.testing.assert_almost_equal(y_fixture.econ.direct_req,
                                       y_fixture.test_derivations.direct_req_matrix,
                                       decimal=4)

    def test_market_share(self, y_fixture):
        assert len(y_fixture.econ.market_share) == y_fixture.industry_count
        np.testing.assert_almost_equal(y_fixture.econ.market_share,
                                       y_fixture.test_derivations.market_share_matrix,
                                       decimal=5)

    def test_tech_coefficient(self, y_fixture):
        assert len(y_fixture.econ.tech_coefficient) == y_fixture.commodity_count
        expected = np.dot(y_fixture.test_derivations.direct_req_matrix,
                          y_fixture.test_derivations.market_share_matrix)
        np.testing.assert_almost_equal(y_fixture.econ.tech_coefficient,
                                       expected,
                                       decimal=4)

    def test_leontief_inverse(self, y_fixture):
        assert len(y_fixture.econ.leontief_inverse) == y_fixture.commodity_count
        assert len(y_fixture.econ.leontief_inverse[0]) == y_fixture.commodity_count
        np.testing.assert_almost_equal(y_fixture.econ.leontief_inverse,
                                       y_fixture.test_derivations.total_req_matrix,
                                       decimal=4)

    def test_total_requirements(self, y_fixture):
        assert len(y_fixture.econ.total_requirements) == y_fixture.commodity_count
        expected = np.dot(y_fixture.test_derivations.total_req_matrix,
                          y_fixture.econ.demand_vector)
        np.testing.assert_allclose(y_fixture.econ.total_requirements,
                                   expected,
                                   rtol=1e-2, atol=0)

    def test_unit_requirements(self, y_fixture):
        assert len(y_fixture.econ.unit_requirements) == y_fixture.commodity_count
        np.testing.assert_almost_equal(y_fixture.econ.unit_requirements,
                                       y_fixture.test_derivations.output_req_vector,
                                       decimal=3)

    def test_unit_price(self, y_fixture):
        assert len(y_fixture.econ.unit_price) == y_fixture.commodity_count
        np.testing.assert_almost_equal(y_fixture.econ.unit_price,
                                       np.ones(y_fixture.commodity_count),
                                       decimal=1)

    # modeling derivations

    def test_tax_matrix(self, y_fixture):
        mock_args = y_fixture.econ.model_args
        expected = np.zeros((y_fixture.commodity_count, y_fixture.industry_count))
        for arg in mock_args:
            commodity, rate = arg
            expected[commodity].fill(rate)
        np.testing.assert_array_equal(y_fixture.econ.tax_matrix, expected)

    def test_tax_coefficient(self, y_fixture):
        assert len(y_fixture.econ.tax_coefficient) == y_fixture.commodity_count

    def test_rel_coefficient(self, y_fixture):
        expected = np.subtract(y_fixture.econ.rel_coefficient,
                                        y_fixture.econ.tax_coefficient)[0]
        assert len(y_fixture.econ.tax_coefficient) == y_fixture.commodity_count
        np.testing.assert_almost_equal(y_fixture.econ.value_coefficient,
                                       expected, decimal=1)

    def test_rel_unit_price(self, y_fixture):
        rel_unit_price = y_fixture.econ.rel_unit_price
        rel_coefficient = np.linalg.lstsq(y_fixture.econ.leontief_inverse_trans, rel_unit_price)[0]
        value_coefficient = np.subtract(rel_coefficient, y_fixture.econ.tax_coefficient)[0]
        asserted = np.dot(y_fixture.econ.leontief_inverse_trans, value_coefficient)[0]
        expected = np.ones(y_fixture.commodity_count)
        assert len(rel_unit_price) == y_fixture.commodity_count
        np.testing.assert_almost_equal(asserted, expected, decimal=1)

    # helper methods

    def test_get_x(self, y_fixture):
        if y_fixture.industry_count == 15:
            assert y_fixture.econ.get_x('Agriculture, forestry, fishing, and hunting') == 0
        elif y_fixture.industry_count == 71:
            assert y_fixture.econ.get_x('Farms') == 0

    def test_get_y(self, y_fixture):
        if y_fixture.commodity_count == 17:
            assert y_fixture.econ.get_y('Agriculture, forestry, fishing, and hunting') == 0
        elif y_fixture.commodity_count == 73:
            assert y_fixture.econ.get_y('Farms') == 0
        penult_item = 'Scrap, used and secondhand goods'
        last_item = 'Noncomparable imports and rest-of-the-world adjustment [1]'
        assert y_fixture.econ.get_y(last_item) == y_fixture.commodity_count - 1
        assert y_fixture.econ.get_y(penult_item) == y_fixture.commodity_count - 2
#
