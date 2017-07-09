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
                                         len(self.make_table)))

    def balance(self):
        self.direct_req = self.derive_direct_req()
        self.market_share = self.derive_market_share()
        self.tech_coefficient = self.derive_tech_coefficient()
        self.tech_coefficient_trans = self.tech_coefficient.transpose()
        self.adjustment = self.derive_adjustment()
        self.value_coefficient = self.derive_value_coefficient()
        self.leontief_inverse = self.derive_leontief_inverse()
        self.leontief_inverse_trans = self.derive_leontief_inverse_trans()
        self.total_requirements = self.derive_total_requirements()
        self.unit_requirements = self.derive_unit_requirements()
        self.unit_price = self.derive_unit_price()

    def model_price(self, args):
        self.rel_price_args = args
        self.tax_matrix = self.derive_tax_matrix(*self.rel_price_args)
        self.tax_coefficient = self.derive_tax_coefficient()
        self.rel_coefficient = self.derive_rel_coefficient()
        self.rel_unit_price = self.derive_rel_unit_price()

    def model_output(self, args):
        self.rel_demand_args = args
        self.demand_argument = self.derive_demand_argument(*self.rel_demand_args)
        self.rel_total_requirements = self.derive_rel_total_requirements()

    # balancing derivations

    def derive_direct_req(self):
        x = np.diag(self.industry_vector)
        y = np.linalg.inv(x)
        z = np.dot(self.use_table, y)
        return z

    def derive_market_share(self):
        x = np.diag(self.commodity_vector)
        y = np.linalg.inv(x)
        z = np.dot(self.make_table, y)
        return z

    def derive_tech_coefficient(self):
        return np.dot(self.direct_req, self.market_share)

    def derive_adjustment(self):
        x = np.diag(self.industry_vector)
        y = np.linalg.inv(x)
        z = np.dot(self.noncomp_vector, y)
        return np.dot(z, self.market_share)

    def derive_value_coefficient(self):
        a = np.diag(self.industry_vector)
        b = np.linalg.inv(a)
        x = np.dot(self.value_vector, b)
        y = np.dot(x, self.market_share)
        z = np.add(y, self.adjustment)
        return z

    def derive_leontief_inverse(self):
        x = np.subtract(self.identity,
                        self.tech_coefficient)
        y = np.linalg.inv(x)
        return y

    def derive_leontief_inverse_trans(self):
        x = np.subtract(self.identity,
                        self.tech_coefficient_trans).astype('float')
        y = np.linalg.inv(x)
        return y

    def derive_total_requirements(self):
        return np.dot(self.leontief_inverse,
                      self.demand_vector)

    def derive_unit_requirements(self):
        return np.sum(self.leontief_inverse_trans, axis=1)

    def derive_unit_price(self):
        return np.dot(self.leontief_inverse_trans,
                      self.value_coefficient)

    # modeling derivations

    def derive_tax_matrix(self, *args):
        cxi_null_matrix = deepcopy(self.cxi_null_matrix)
        for arg in args:
            commodity, rate = arg
            cxi_null_matrix[commodity].fill(rate)
        tax_matrix = cxi_null_matrix
        return tax_matrix

    def derive_tax_coefficient(self):
        a = np.multiply(self.use_table, self.tax_matrix)
        b = np.linalg.inv(np.diag(self.industry_vector))
        c = np.dot(a, b)
        x = np.dot(c, self.market_share)
        y = x.transpose()
        z = np.ones((len(self.use_table), 1))
        q = np.dot(y, z)
        return q

    def derive_rel_coefficient(self):
        return np.add(self.value_coefficient, self.tax_coefficient)

    def derive_rel_unit_price(self):
        return np.dot(self.leontief_inverse_trans,
                      self.rel_coefficient)

    def derive_demand_argument(self, *args):
        demand = deepcopy(self.demand_vector)
        for arg in args:
            commodity, delta = arg
            demand[commodity][0] = demand[commodity][0] + delta
        return demand

    def derive_rel_total_requirements(self):
        return np.dot(self.leontief_inverse,
                      self.demand_argument)

    # helper methods

    def get_x(self, name):
        return self.industry_legend.index(name)

    def get_y(self, name):
        return self.commodity_legend.index(name)
#
