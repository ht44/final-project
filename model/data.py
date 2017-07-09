#
import os
import pandas as pd

class Dataset:
    def __init__(self, level='sector', year='2015'):

        use_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'use.pkl'))
        make_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'make.pkl'))
        value_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'value.pkl'))
        industry_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'industry.pkl'))
        noncomp_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'noncomp.pkl'))
        commodity_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'commodity.pkl'))
        demand_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'demand.pkl'))

        self.use_matrix = use_df.as_matrix().astype('float')
        self.make_matrix = make_df.as_matrix().astype('float')
        self.value_vector = value_df.as_matrix()[0].astype('float')
        self.industry_vector = industry_df.as_matrix()[0].astype('float')
        self.commodity_vector = commodity_df.as_matrix()[0].astype('float')
        self.demand_vector = demand_df.as_matrix().astype('float')
        self.noncomp_vector = noncomp_df.as_matrix()[0].astype('float')
        self.industry_legend = use_df.columns.tolist()
        self.commodity_legend = use_df.index.tolist()
#
