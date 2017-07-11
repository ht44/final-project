from .models import *
from iomodel import model

class Seed:
    def __init__(self):
        pass

    def del_records(self, level):
        if level == 'sector':
            SectorUse.objects.all().delete()
            SectorMake.objects.all().delete()
            SectorValue.objects.all().delete()
            SectorIndustry.objects.all().delete()
            SectorCommodity.objects.all().delete()
            SectorDemand.objects.all().delete()
            SectorNoncomp.objects.all().delete()
        elif level == 'summary':
            SummaryUse.objects.all().delete()
            SummaryMake.objects.all().delete()
            SummaryValue.objects.all().delete()
            SummaryIndustry.objects.all().delete()
            SummaryCommodity.objects.all().delete()
            SummaryDemand.objects.all().delete()
            SummaryNoncomp.objects.all().delete()

    def run_seeds(self, level):
        if level == 'sector':
            self.seed_use(SectorUse, level)
            self.seed_make(SectorMake, level)
            self.seed_value(SectorValue, level)
            self.seed_industry(SectorIndustry, level)
            self.seed_commodity(SectorCommodity, level)
            self.seed_demand(SectorDemand, level)
            self.seed_noncomp(SectorNoncomp, level)
        elif level == 'summary':
            self.seed_use(SummaryUse, level)
            self.seed_make(SummaryMake, level)
            self.seed_value(SummaryValue, level)
            self.seed_industry(SummaryIndustry, level)
            self.seed_commodity(SummaryCommodity, level)
            self.seed_demand(SummaryDemand, level)
            self.seed_noncomp(SummaryNoncomp, level)

    def seed_use(self, table, level):
        for y in range(1997, 2016):
            econ = model.Leontief(level, str(y))
            for i in range(len(econ.use_matrix)):
                for j in range(len(econ.use_matrix[i])):
                    newrec = table(
                        col=j, row=i, val=econ.use_matrix[i][j], year=y)
                    newrec.save()
        del newrec
        del econ

    def seed_make(self, table, level):
        for y in range(1997, 2016):
            econ = model.Leontief(level, str(y))
            for i in range(len(econ.make_matrix)):
                for j in range(len(econ.make_matrix[i])):
                    newrec = table(
                        col=j, row=i, val=econ.make_matrix[i][j], year=y)
                    newrec.save()
        del newrec
        del econ


    def seed_value(self, table, level):
        for y in range(1997, 2016):
            econ = model.Leontief(level, str(y))
            for i in range(len(econ.value_vector)):
                newrec = table(
                    col=i, row=0, val=econ.value_vector[i], year=y)
                newrec.save()
        del newrec
        del econ

    def seed_industry(self, table, level):
        for y in range(1997, 2016):
            econ = model.Leontief(level, str(y))
            for i in range(len(econ.industry_vector)):
                newrec = table(
                    col=i, row=0, val=econ.industry_vector[i], year=y)
                newrec.save()
        del newrec
        del econ

    def seed_commodity(self, table, level):
        for y in range(1997, 2016):
            econ = model.Leontief(level, str(y))
            for i in range(len(econ.commodity_vector)):
                newrec = table(
                    col=i, row=0, val=econ.commodity_vector[i], year=y)
                newrec.save()
        del newrec
        del econ

    def seed_noncomp(self, table, level):
        for y in range(1997, 2016):
            econ = model.Leontief(level, str(y))
            for i in range(len(econ.noncomp_vector)):
                newrec = table(
                    col=i, row=0, val=econ.noncomp_vector[i], year=y)
                newrec.save()
        del newrec
        del econ

    def seed_demand(self, table, level):
        for y in range(1997, 2016):
            econ = model.Leontief(level, str(y))
            for i in range(len(econ.demand_vector)):
                newrec = table(
                    col=0, row=i, val=econ.demand_vector[i][0], year=y)
                newrec.save()
        del newrec
        del econ

seed = Seed()
