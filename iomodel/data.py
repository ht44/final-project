#
import os
import pandas as pd

import sqlalchemy

engine = sqlalchemy.create_engine(
    'postgresql://hayden:passworddev@localhost/iom_site')

class Dataset:
    def __init__(self, level='sector', year='2015', sql=True):

        # if sql == True:
        u = pd.read_sql(
            f'SELECT * FROM dash_{level}use WHERE year={year}',
                engine).pivot(index='row', columns='col', values='val')
        m = pd.read_sql(
            f'SELECT * FROM dash_{level}make WHERE year={year}',
                engine).pivot(index='row', columns='col', values='val')
        i = pd.read_sql(
            f'SELECT * FROM dash_{level}industry WHERE year={year}',
                engine).pivot(index='row', columns='col', values='val')
        c = pd.read_sql(
            f'SELECT * FROM dash_{level}commodity WHERE year={year}',
                engine).pivot(index='row', columns='col', values='val')
        v = pd.read_sql(
            f'SELECT * FROM dash_{level}value WHERE year={year}',
                engine).pivot(index='row', columns='col', values='val')
        d = pd.read_sql(
            f'SELECT * FROM dash_{level}demand WHERE year={year}',
                engine).pivot(index='row', columns='col', values='val')
        n = pd.read_sql(
            f'SELECT * FROM dash_{level}noncomp WHERE year={year}',
                engine).pivot(index='row', columns='col', values='val')


        # else:
        #     u = pd.read_pickle(
        #         os.path.join(
        #             os.path.dirname(__file__),'pickles', level, year, 'use.pkl'))
        #     m = pd.read_pickle(
        #         os.path.join(
        #             os.path.dirname(__file__),'pickles', level, year, 'make.pkl'))
        #     v = pd.read_pickle(
        #         os.path.join(
        #             os.path.dirname(__file__),'pickles', level, year, 'value.pkl'))
        #     i = pd.read_pickle(
        #         os.path.join(
        #             os.path.dirname(__file__),'pickles', level, year, 'industry.pkl'))
        #     n = pd.read_pickle(
        #         os.path.join(
        #             os.path.dirname(__file__),'pickles', level, year, 'noncomp.pkl'))
        #     c = pd.read_pickle(
        #         os.path.join(
        #             os.path.dirname(__file__),'pickles', level, year, 'commodity.pkl'))
        #     d = pd.read_pickle(
        #         os.path.join(
        #             os.path.dirname(__file__),'pickles', level, year, 'demand.pkl'))

        self.use_matrix = u.as_matrix().astype('float')
        self.make_matrix = m.as_matrix().astype('float')
        self.value_vector = v.as_matrix()[0].astype('float')
        self.industry_vector = i.as_matrix()[0].astype('float')
        self.commodity_vector = c.as_matrix()[0].astype('float')
        self.demand_vector = d.as_matrix().astype('float')
        self.noncomp_vector = n.as_matrix()[0].astype('float')
        # self.commodity_legend = u.index.tolist()
#
