#
import numpy as np
from copy import deepcopy

class Leontief:
    def __init__(self, dataset):
        self.make_table = deepcopy(dataset.make_table)
        self.use_table = deepcopy(dataset.use_table)
        self.industry_legend = deepcopy(dataset.industry_legend)
        self.commodity_legend = deepcopy(dataset.commodity_legend)
        self.industry_vector = deepcopy(dataset.industry_vector)
        self.commodity_vector = deepcopy(dataset.commodity_vector)
        self.value_vector = deepcopy(dataset.value_vector)
        self.demand_vector = deepcopy(dataset.demand_vector)
        self.noncomp_vector = deepcopy(dataset.noncomp_vector)
        self.identity = np.identity(len(self.use_table))
        self.size = len(self.make_table)
        self.cxi_null_matrix = np.zeros((len(self.use_table),
                                         len(self.make_table)
                                         ))

    def balance(self):
        self.direct_req = self.derive_direct_req(
            self.industry_vector, self.use_table)
        self.market_share = self.derive_market_share(
            self.commodity_vector, self.make_table)
        self.tech_coefficient = self.derive_tech_coefficient(
            self.direct_req, self.market_share)
        self.tech_coefficient_trans = self.tech_coefficient.transpose()
        self.adjustment = self.derive_adjustment(
            self.industry_vector, self.noncomp_vector, self.market_share)
        self.value_coefficient = self.derive_value_coefficient(
            self.industry_vector, self.value_vector, self.market_share, self.adjustment)
        self.leontief_inverse = self.derive_leontief_inverse(
            self.identity, self.tech_coefficient)
        self.leontief_inverse_trans = self.derive_leontief_inverse_trans(
            self.identity, self.tech_coefficient_trans)
        self.total_requirements = self.derive_total_requirements(
            self.leontief_inverse, self.demand_vector)
        self.unit_requirements = self.derive_unit_requirements(
            self.leontief_inverse_trans)
        self.unit_price = self.derive_unit_price(
            self.leontief_inverse_trans, self.value_coefficient)

    def model_price(self, args):
        self.rel_price_args = self.process_args(args)
        self.tax_matrix = self.derive_tax_matrix(
            *self.rel_price_args)
        self.tax_coefficient = self.derive_tax_coefficient(
            self.use_table, self.tax_matrix, self.industry_vector, self.market_share)
        self.rel_coefficient = self.derive_rel_coefficient(
            self.value_coefficient, self.tax_coefficient)
        self.rel_unit_price = self.derive_rel_unit_price(
            self.leontief_inverse_trans, self.rel_coefficient)

    def model_output(self, args):
        self.rel_demand_args = self.process_args(args)
        self.demand_argument = self.derive_demand_argument(
            self.demand_vector, *self.rel_demand_args)
        self.rel_total_requirements = self.derive_rel_total_requirements(
            self.leontief_inverse, self.demand_argument)

    # balancing derivations

    def derive_direct_req(
        self, industry_vector, use_table):
        x = np.diag(industry_vector)
        y = np.linalg.inv(x)
        z = np.dot(use_table, y)
        return z

    def derive_market_share(
        self, commodity_vector, make_table):
        x = np.diag(commodity_vector)
        y = np.linalg.inv(x)
        z = np.dot(make_table, y)
        return z

    def derive_tech_coefficient(
        self, direct_req, market_share):
        return np.dot(direct_req, market_share)

    def derive_adjustment(
        self, industry_vector, noncomp_vector, market_share):
        x = np.diag(industry_vector)
        y = np.linalg.inv(x)
        z = np.dot(noncomp_vector, y)
        return np.dot(z, market_share)

    def derive_value_coefficient(
        self, industry_vector, value_vector, market_share, adjustment):
        a = np.diag(industry_vector)
        b = np.linalg.inv(a)
        x = np.dot(value_vector, b)
        y = np.dot(x, market_share)
        z = np.add(y, adjustment)
        return z

    def derive_leontief_inverse(
        self, identity, tech_coefficient):
        x = np.subtract(identity,
                        tech_coefficient)
        y = np.linalg.inv(x)
        return y

    def derive_leontief_inverse_trans(
        self, identity, tech_coefficient_trans):
        x = np.subtract(identity,
                        tech_coefficient_trans).astype('float')
        y = np.linalg.inv(x)
        return y

    def derive_total_requirements(
        self, leontief_inverse, demand_vector):
        return np.dot(leontief_inverse,
                      demand_vector)

    def derive_unit_requirements(
        self, leontief_inverse_trans):
        return np.sum(leontief_inverse_trans, axis=1)

    def derive_unit_price(
        self, leontief_inverse_trans, value_coefficient):
        return np.dot(leontief_inverse_trans,
                      value_coefficient)

    # modeling derivations

    def derive_tax_matrix(self, *args):
        cxi_null_matrix = deepcopy(self.cxi_null_matrix)
        for arg in args:
            commodity, rate = arg
            cxi_null_matrix[commodity].fill(rate)
        tax_matrix = cxi_null_matrix
        return tax_matrix

    def derive_tax_coefficient(
        self, use_table, tax_matrix, industry_vector, market_share):
        a = np.multiply(use_table, tax_matrix)
        b = np.linalg.inv(np.diag(industry_vector))
        c = np.dot(a, b)
        x = np.dot(c, market_share)
        y = x.transpose()
        z = np.ones((len(use_table), 1))
        q = np.dot(y, z)
        return q

    def derive_rel_coefficient(
        self, value_coefficient, tax_coefficient):
        return np.add(value_coefficient, tax_coefficient)

    def derive_rel_unit_price(
        self, leontief_inverse_trans, rel_coefficient):
        return np.dot(leontief_inverse_trans,
                      rel_coefficient)

    def derive_demand_argument(
        self, demand_vector, *args):
        demand = deepcopy(demand_vector)
        for arg in args:
            commodity, delta = arg
            demand[commodity][0] = demand[commodity][0] + delta
        return demand

    def derive_rel_total_requirements(
        self, leontief_inverse, demand_argument):
        return np.dot(leontief_inverse,
                      demand_argument)

    # helper methods

    def get_x(self, name):
        return self.industry_legend.index(name)

    def get_y(self, name):
        return self.commodity_legend.index(name)

    def process_args(self, args):
        for a in range(len(args)):
            if type(args[a][0]) == str:
                key = self.get_y(args[a][0])
                val = args[a][1]
                args[a] = key, val
        return args
#
