#
import pytest
import numpy as np

class TestModel(object):

    # inputs

    def test_model_size(self, fixture):
        assert fixture.econ.size == fixture.industry_count

    def test_use_table(self, fixture):
        assert len(fixture.econ.use_table) == fixture.commodity_count
        assert len(fixture.econ.use_table[0]) == fixture.industry_count

    def test_make_table(self, fixture):
        assert len(fixture.econ.make_table) == fixture.industry_count
        assert len(fixture.econ.make_table[0]) == fixture.commodity_count

    def test_industry_vector(self, fixture):
        assert len(fixture.econ.industry_vector) == fixture.industry_count

    def test_commodity_vector(self, fixture):
        assert len(fixture.econ.commodity_vector) == fixture.commodity_count

    def test_value_vector(self, fixture):
        assert len(fixture.econ.value_vector) == fixture.industry_count

    def test_noncomp_vector(self, fixture):
        assert len(fixture.econ.noncomp_vector) == fixture.industry_count

    def test_demand_vector(self, fixture):
        assert len(fixture.econ.demand_vector) == fixture.commodity_count
        assert len(fixture.econ.demand_vector[0]) == 1

    def test_identity(self, fixture):
        assert len(fixture.econ.identity) == fixture.commodity_count
        assert len(fixture.econ.identity[0]) == fixture.commodity_count

    # derivations

    def test_direct_req(self, fixture):
        assert len(fixture.econ.direct_req) == fixture.commodity_count
        np.testing.assert_almost_equal(fixture.econ.direct_req,
                                       fixture.test_derivations.direct_req_matrix,
                                       decimal=4)

    def test_market_share(self, fixture):
        assert len(fixture.econ.market_share) == fixture.industry_count
        np.testing.assert_almost_equal(fixture.econ.market_share,
                                       fixture.test_derivations.market_share_matrix,
                                       decimal=5)

    def test_tech_coefficient(self, fixture):
        assert len(fixture.econ.tech_coefficient) == fixture.commodity_count
        expected = np.dot(fixture.test_derivations.direct_req_matrix,
                          fixture.test_derivations.market_share_matrix)
        np.testing.assert_almost_equal(fixture.econ.tech_coefficient,
                                       expected,
                                       decimal=4)

    def test_leontief_inverse(self, fixture):
        assert len(fixture.econ.leontief_inverse) == fixture.commodity_count
        assert len(fixture.econ.leontief_inverse[0]) == fixture.commodity_count
        np.testing.assert_almost_equal(fixture.econ.leontief_inverse,
                                       fixture.test_derivations.total_req_matrix,
                                       decimal=4)

    def test_total_requirements(self, fixture):
        assert len(fixture.econ.total_requirements) == fixture.commodity_count
        expected = np.dot(fixture.test_derivations.total_req_matrix,
                          fixture.econ.demand_vector)
        np.testing.assert_allclose(fixture.econ.total_requirements,
                                   expected,
                                   rtol=1e-2, atol=0)

    def test_unit_requirements(self, fixture):
        assert len(fixture.econ.unit_requirements) == fixture.commodity_count
        np.testing.assert_almost_equal(fixture.econ.unit_requirements,
                                       fixture.test_derivations.output_req_vector,
                                       decimal=3)

    def test_unit_price(self, fixture):
        assert len(fixture.econ.unit_price) == fixture.commodity_count
        np.testing.assert_almost_equal(fixture.econ.unit_price,
                                       np.ones(fixture.commodity_count),
                                       decimal=1)

    def test_industry_legend(self, fixture):
        assert len(fixture.econ.industry_legend) == fixture.industry_count
        if fixture.industry_count == 15:
            assert fixture.econ.industry_legend[0] == 'Agriculture, forestry, fishing, and hunting'
        elif fixture.industry_count == 71:
            assert fixture.econ.industry_legend[0] == 'Farms'

    def test_commodity_legend(self, fixture):
        assert len(fixture.econ.commodity_legend) == fixture.commodity_count
        if fixture.commodity_count == 17:
            assert fixture.econ.commodity_legend[0] == 'Agriculture, forestry, fishing, and hunting'
        elif fixture.commodity_count == 73:
            assert fixture.econ.commodity_legend[0] == 'Farms'
        penult_idx = fixture.commodity_count - 2
        last_idx = fixture.commodity_count - 1
        assert fixture.econ.commodity_legend[penult_idx] == 'Scrap, used and secondhand goods'
        assert fixture.econ.commodity_legend[last_idx] == 'Noncomparable imports and rest-of-the-world adjustment [1]'

    def test_get_x(self, fixture):
        if fixture.industry_count == 15:
            assert fixture.econ.get_x('Agriculture, forestry, fishing, and hunting') == 0
        elif fixture.industry_count == 71:
            assert fixture.econ.get_x('Farms') == 0

    def test_get_y(self, fixture):
        if fixture.commodity_count == 17:
            assert fixture.econ.get_y('Agriculture, forestry, fishing, and hunting') == 0
        elif fixture.commodity_count == 73:
            assert fixture.econ.get_y('Farms') == 0
        penult_item = 'Scrap, used and secondhand goods'
        last_item = 'Noncomparable imports and rest-of-the-world adjustment [1]'
        assert fixture.econ.get_y[last_item] == fixture.commodity_count - 1
        assert fixture.econ.get_y[penult_item] == fixture.commodity_count - 2
