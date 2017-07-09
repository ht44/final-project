#
import random
import pytest
import numpy as np

class TestEachYear(object):

    # inputs

    def test_model_size(self, multi_year):
        assert multi_year.econ.size == multi_year.industry_count

    def test_use_table(self, multi_year):
        assert len(multi_year.econ.use_table) == multi_year.commodity_count
        assert len(multi_year.econ.use_table[0]) == multi_year.industry_count

    def test_make_table(self, multi_year):
        assert len(multi_year.econ.make_table) == multi_year.industry_count
        assert len(multi_year.econ.make_table[0]) == multi_year.commodity_count

    def test_industry_vector(self, multi_year):
        assert len(multi_year.econ.industry_vector) == multi_year.industry_count

    def test_commodity_vector(self, multi_year):
        assert len(multi_year.econ.commodity_vector) == multi_year.commodity_count

    def test_value_vector(self, multi_year):
        assert len(multi_year.econ.value_vector) == multi_year.industry_count

    def test_noncomp_vector(self, multi_year):
        assert len(multi_year.econ.noncomp_vector) == multi_year.industry_count

    def test_demand_vector(self, multi_year):
        assert len(multi_year.econ.demand_vector) == multi_year.commodity_count
        assert len(multi_year.econ.demand_vector[0]) == 1

    def test_identity(self, multi_year):
        assert len(multi_year.econ.identity) == multi_year.commodity_count
        assert len(multi_year.econ.identity[0]) == multi_year.commodity_count

    def test_industry_legend(self, multi_year):
        assert len(multi_year.econ.industry_legend) == multi_year.industry_count
        if multi_year.industry_count == 15:
            assert multi_year.econ.industry_legend[0] == 'Agriculture, forestry, fishing, and hunting'
        elif multi_year.industry_count == 71:
            assert multi_year.econ.industry_legend[0] == 'Farms'

    def test_commodity_legend(self, multi_year):
        assert len(multi_year.econ.commodity_legend) == multi_year.commodity_count
        if multi_year.commodity_count == 17:
            assert multi_year.econ.commodity_legend[0] == 'Agriculture, forestry, fishing, and hunting'
        elif multi_year.commodity_count == 73:
            assert multi_year.econ.commodity_legend[0] == 'Farms'
        penult_idx = multi_year.commodity_count - 2
        last_idx = multi_year.commodity_count - 1
        assert multi_year.econ.commodity_legend[penult_idx] == 'Scrap, used and secondhand goods'
        assert multi_year.econ.commodity_legend[last_idx] == 'Noncomparable imports and rest-of-the-world adjustment [1]'

    def test_cxi_null_matrix(self, multi_year):
        assert len(multi_year.econ.cxi_null_matrix) == multi_year.commodity_count
        assert len(multi_year.econ.cxi_null_matrix[0]) == multi_year.industry_count
        expected = np.zeros((multi_year.commodity_count, multi_year.industry_count))
        np.testing.assert_array_equal(multi_year.econ.cxi_null_matrix, expected)

    # balancing derivations

    def test_direct_req(self, multi_year):
        assert len(multi_year.econ.direct_req) == multi_year.commodity_count
        np.testing.assert_almost_equal(multi_year.econ.direct_req,
                                       multi_year.test_derivations.direct_req_matrix,
                                       decimal=4)

    def test_market_share(self, multi_year):
        assert len(multi_year.econ.market_share) == multi_year.industry_count
        np.testing.assert_almost_equal(multi_year.econ.market_share,
                                       multi_year.test_derivations.market_share_matrix,
                                       decimal=5)

    def test_tech_coefficient(self, multi_year):
        assert len(multi_year.econ.tech_coefficient) == multi_year.commodity_count
        expected = np.dot(multi_year.test_derivations.direct_req_matrix,
                          multi_year.test_derivations.market_share_matrix)
        np.testing.assert_almost_equal(multi_year.econ.tech_coefficient,
                                       expected,
                                       decimal=4)

    def test_leontief_inverse(self, multi_year):
        assert len(multi_year.econ.leontief_inverse) == multi_year.commodity_count
        assert len(multi_year.econ.leontief_inverse[0]) == multi_year.commodity_count
        np.testing.assert_almost_equal(multi_year.econ.leontief_inverse,
                                       multi_year.test_derivations.total_req_matrix,
                                       decimal=4)

    def test_total_requirements(self, multi_year):
        assert len(multi_year.econ.total_requirements) == multi_year.commodity_count

        asserted = multi_year.econ.total_requirements
        expected = np.dot(multi_year.test_derivations.total_req_matrix,
                          multi_year.test_derivations.demand_vector)

        np.testing.assert_allclose(asserted, expected, rtol=1e-2)

    def test_unit_requirements(self, multi_year):
        assert len(multi_year.econ.unit_requirements) == multi_year.commodity_count
        np.testing.assert_almost_equal(multi_year.econ.unit_requirements,
                                       multi_year.test_derivations.output_req_vector,
                                       decimal=3)

    def test_unit_price(self, multi_year):
        assert len(multi_year.econ.unit_price) == multi_year.commodity_count
        np.testing.assert_almost_equal(multi_year.econ.unit_price,
                                       np.ones(multi_year.commodity_count),
                                       decimal=1)

    # modeling derivations

    def test_tax_matrix(self, multi_year):
        mock_args = multi_year.econ.rel_price_args
        expected = np.zeros((multi_year.commodity_count, multi_year.industry_count))
        for arg in mock_args:
            commodity, rate = arg
            expected[commodity].fill(rate)
        np.testing.assert_array_equal(multi_year.econ.tax_matrix, expected)

    def test_tax_coefficient(self, multi_year):
        assert len(multi_year.econ.tax_coefficient) == multi_year.commodity_count

    def test_rel_coefficient(self, multi_year):
        expected = np.subtract(multi_year.econ.rel_coefficient,
                                        multi_year.econ.tax_coefficient)[0]
        assert len(multi_year.econ.tax_coefficient) == multi_year.commodity_count
        np.testing.assert_almost_equal(multi_year.econ.value_coefficient,
                                       expected, decimal=1)

    def test_rel_unit_price(self, multi_year):
        rel_unit_price = multi_year.econ.rel_unit_price
        rel_coefficient = np.linalg.lstsq(multi_year.econ.leontief_inverse_trans, rel_unit_price)[0]
        value_coefficient = np.subtract(rel_coefficient, multi_year.econ.tax_coefficient)[0]
        asserted = np.dot(multi_year.econ.leontief_inverse_trans, value_coefficient)[0]
        expected = np.ones(multi_year.commodity_count)
        assert len(rel_unit_price) == multi_year.commodity_count
        np.testing.assert_almost_equal(asserted, expected, decimal=1)

    def test_demand_argument(self, multi_year):

        mock_args = multi_year.econ.rel_demand_args

        assert len(mock_args) == len(multi_year.econ.rel_price_args)
        assert mock_args[0][1] < 0
        assert mock_args[2][1] < 0
        assert mock_args[1][1] > 0
        assert mock_args[3][1] > 0

        asserted = multi_year.econ.demand_argument
        expected = multi_year.test_derivations.demand_vector
        for arg in mock_args:
            commodity, delta = arg
            expected[commodity][0] = expected[commodity][0] + delta

        np.testing.assert_almost_equal(asserted, expected, decimal=1)

    def test_rel_total_requirements(self, multi_year):
        assert len(multi_year.econ.rel_total_requirements) == multi_year.commodity_count

        asserted = multi_year.econ.rel_total_requirements
        expected = np.dot(multi_year.test_derivations.total_req_matrix,
                          multi_year.econ.demand_argument)

        np.testing.assert_allclose(asserted, expected, rtol=1e-2)

    # helper methods

    def test_get_x(self, multi_year):
        if multi_year.industry_count == 15:
            assert multi_year.econ.get_x('Agriculture, forestry, fishing, and hunting') == 0
        elif multi_year.industry_count == 71:
            assert multi_year.econ.get_x('Farms') == 0

    def test_get_y(self, multi_year):
        if multi_year.commodity_count == 17:
            assert multi_year.econ.get_y('Agriculture, forestry, fishing, and hunting') == 0
        elif multi_year.commodity_count == 73:
            assert multi_year.econ.get_y('Farms') == 0
        penult_item = 'Scrap, used and secondhand goods'
        last_item = 'Noncomparable imports and rest-of-the-world adjustment [1]'
        assert multi_year.econ.get_y(last_item) == multi_year.commodity_count - 1
        assert multi_year.econ.get_y(penult_item) == multi_year.commodity_count - 2

    def test_process_args(self, multi_year):

        names = multi_year.econ.commodity_legend
        nums = [i for i in range(multi_year.commodity_count)]
        vals = [random.random() for j in range(multi_year.commodity_count)]

        asserted = multi_year.econ.process_args(list(zip(names, vals)))
        expected = list(zip(nums, vals))

        assert asserted == expected
