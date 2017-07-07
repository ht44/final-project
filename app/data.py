#
import os
import numpy as np
import pandas as pd
from copy import deepcopy

class Dataset:
    def __init__(self, level, year):

        self.use_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'use.pkl'))
        self.make_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'make.pkl'))
        self.value_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'value.pkl'))
        self.industry_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'industry.pkl'))
        self.noncomp_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'noncomp.pkl'))
        self.commodity_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'commodity.pkl'))
        self.demand_df = pd.read_pickle(
            os.path.join(
                os.path.dirname(__file__),'pickles', level, year, 'demand.pkl'))

        self.use_table = self.use_df.as_matrix().astype('float')
        self.make_table = self.make_df.as_matrix().astype('float')
        self.value_vector = self.value_df.as_matrix()[0].astype('float')
        self.industry_vector = self.industry_df.as_matrix()[0].astype('float')
        self.commodity_vector = self.commodity_df.as_matrix()[0].astype('float')
        self.demand_vector = self.demand_df.as_matrix().astype('float')
        self.noncomp_vector = self.noncomp_df.as_matrix()[0].astype('float')
        self.industry_legend = self.use_df.columns
        self.commodity_legend = self.use_df.index
#
