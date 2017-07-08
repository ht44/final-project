#

import pytest
import numpy as np

class TestYear(object):

    # inputs

    def test_model_size(self, single_year):
        assert single_year.econ.size == single_year.industry_count

    def test_use_table(self, single_year):
        assert len(single_year.econ.use_table) == single_year.commodity_count
        assert len(single_year.econ.use_table[0]) == single_year.industry_count

    def test_make_table(self, single_year):
        assert len(single_year.econ.make_table) == single_year.industry_count
        assert len(single_year.econ.make_table[0]) == single_year.commodity_count

    def test_industry_vector(self, single_year):
        assert len(single_year.econ.industry_vector) == single_year.industry_count

    def test_commodity_vector(self, single_year):
        assert len(single_year.econ.commodity_vector) == single_year.commodity_count

    def test_value_vector(self, single_year):
        assert len(single_year.econ.value_vector) == single_year.industry_count

    def test_noncomp_vector(self, single_year):
        assert len(single_year.econ.noncomp_vector) == single_year.industry_count

    def test_demand_vector(self, single_year):
        assert len(single_year.econ.demand_vector) == single_year.commodity_count
        assert len(single_year.econ.demand_vector[0]) == 1

    def test_identity(self, single_year):
        assert len(single_year.econ.identity) == single_year.commodity_count
        assert len(single_year.econ.identity[0]) == single_year.commodity_count

    def test_industry_legend(self, single_year):
        assert len(single_year.econ.industry_legend) == single_year.industry_count
        if single_year.industry_count == 15:
            assert single_year.econ.industry_legend[0] == 'Agriculture, forestry, fishing, and hunting'
        elif single_year.industry_count == 71:
            assert single_year.econ.industry_legend[0] == 'Farms'

    def test_commodity_legend(self, single_year):
        assert len(single_year.econ.commodity_legend) == single_year.commodity_count
        if single_year.commodity_count == 17:
            assert single_year.econ.commodity_legend[0] == 'Agriculture, forestry, fishing, and hunting'
        elif single_year.commodity_count == 73:
            assert single_year.econ.commodity_legend[0] == 'Farms'
        penult_idx = single_year.commodity_count - 2
        last_idx = single_year.commodity_count - 1
        assert single_year.econ.commodity_legend[penult_idx] == 'Scrap, used and secondhand goods'
        assert single_year.econ.commodity_legend[last_idx] == 'Noncomparable imports and rest-of-the-world adjustment [1]'

    def test_cxi_null_matrix(self, single_year):
        assert len(single_year.econ.cxi_null_matrix) == single_year.commodity_count
        assert len(single_year.econ.cxi_null_matrix[0]) == single_year.industry_count
        expected = np.zeros((single_year.commodity_count, single_year.industry_count))
        np.testing.assert_array_equal(single_year.econ.cxi_null_matrix, expected)

    # balancing derivations

    def test_direct_req(self, single_year):
        assert len(single_year.econ.direct_req) == single_year.commodity_count
        np.testing.assert_almost_equal(single_year.econ.direct_req,
                                       single_year.test_derivations.direct_req_matrix,
                                       decimal=4)

    def test_market_share(self, single_year):
        assert len(single_year.econ.market_share) == single_year.industry_count
        np.testing.assert_almost_equal(single_year.econ.market_share,
                                       single_year.test_derivations.market_share_matrix,
                                       decimal=5)

    def test_tech_coefficient(self, single_year):
        assert len(single_year.econ.tech_coefficient) == single_year.commodity_count
        expected = np.dot(single_year.test_derivations.direct_req_matrix,
                          single_year.test_derivations.market_share_matrix)
        np.testing.assert_almost_equal(single_year.econ.tech_coefficient,
                                       expected,
                                       decimal=4)

    def test_leontief_inverse(self, single_year):
        assert len(single_year.econ.leontief_inverse) == single_year.commodity_count
        assert len(single_year.econ.leontief_inverse[0]) == single_year.commodity_count
        np.testing.assert_almost_equal(single_year.econ.leontief_inverse,
                                       single_year.test_derivations.total_req_matrix,
                                       decimal=4)

    def test_total_requirements(self, single_year):
        assert len(single_year.econ.total_requirements) == single_year.commodity_count

        asserted = single_year.econ.total_requirements
        expected = np.dot(single_year.test_derivations.total_req_matrix,
                          single_year.test_derivations.demand_vector)

        np.testing.assert_allclose(asserted, expected, rtol=1e-2)

    def test_unit_requirements(self, single_year):
        assert len(single_year.econ.unit_requirements) == single_year.commodity_count
        np.testing.assert_almost_equal(single_year.econ.unit_requirements,
                                       single_year.test_derivations.output_req_vector,
                                       decimal=3)

    def test_unit_price(self, single_year):
        assert len(single_year.econ.unit_price) == single_year.commodity_count
        np.testing.assert_almost_equal(single_year.econ.unit_price,
                                       np.ones(single_year.commodity_count),
                                       decimal=1)

    # modeling derivations

    def test_tax_matrix(self, single_year):
        mock_args = single_year.econ.model_args
        expected = np.zeros((single_year.commodity_count, single_year.industry_count))
        for arg in mock_args:
            commodity, rate = arg
            expected[commodity].fill(rate)
        np.testing.assert_array_equal(single_year.econ.tax_matrix, expected)

    def test_tax_coefficient(self, single_year):
        assert len(single_year.econ.tax_coefficient) == single_year.commodity_count

    def test_rel_coefficient(self, single_year):
        expected = np.subtract(single_year.econ.rel_coefficient,
                                        single_year.econ.tax_coefficient)[0]
        assert len(single_year.econ.tax_coefficient) == single_year.commodity_count
        np.testing.assert_almost_equal(single_year.econ.value_coefficient,
                                       expected, decimal=1)

    def test_rel_unit_price(self, single_year):
        rel_unit_price = single_year.econ.rel_unit_price
        rel_coefficient = np.linalg.lstsq(single_year.econ.leontief_inverse_trans, rel_unit_price)[0]
        value_coefficient = np.subtract(rel_coefficient, single_year.econ.tax_coefficient)[0]
        asserted = np.dot(single_year.econ.leontief_inverse_trans, value_coefficient)[0]
        expected = np.ones(single_year.commodity_count)
        assert len(rel_unit_price) == single_year.commodity_count
        np.testing.assert_almost_equal(asserted, expected, decimal=1)

    def test_demand_argument(self, single_year):

        mock_args = [(0, -500), (1, 300), (2, 99)]
        single_year.econ.model_output(mock_args)

        asserted = single_year.econ.demand_argument
        expected = single_year.test_derivations.demand_vector
        for arg in mock_args:
            commodity, delta = arg
            expected[commodity][0] = expected[commodity][0] + delta

        np.testing.assert_almost_equal(asserted, expected, decimal=1)

    # helper methods

    def test_get_x(self, single_year):
        if single_year.industry_count == 15:
            assert single_year.econ.get_x('Agriculture, forestry, fishing, and hunting') == 0
        elif single_year.industry_count == 71:
            assert single_year.econ.get_x('Farms') == 0

    def test_get_y(self, single_year):
        if single_year.commodity_count == 17:
            assert single_year.econ.get_y('Agriculture, forestry, fishing, and hunting') == 0
        elif single_year.commodity_count == 73:
            assert single_year.econ.get_y('Farms') == 0
        penult_item = 'Scrap, used and secondhand goods'
        last_item = 'Noncomparable imports and rest-of-the-world adjustment [1]'
        assert single_year.econ.get_y(last_item) == single_year.commodity_count - 1
        assert single_year.econ.get_y(penult_item) == single_year.commodity_count - 2
#
