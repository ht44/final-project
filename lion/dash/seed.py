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

    def seed_legend(self, level):
        if level == 'sector':
            names = ['Agriculture, forestry, fishing, and hunting', 'Mining', 'Utilities',
                    'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade',
                    'Transportation and warehousing', 'Information',
                    'Finance, insurance, real estate, rental, and leasing',
                    'Professional and business services',
                    'Educational services, health care, and social assistance',
                    'Arts, entertainment, recreation, accommodation, and food services',
                    'Other services, except government', 'Government',
                    'Scrap, used and secondhand goods',
                    'Noncomparable imports and rest-of-the-world adjustment']

        elif level == 'summary':
            names = ['Farms', 'Forestry, fishing, and related activities',
                       'Oil and gas extraction', 'Mining, except oil and gas',
                       'Support activities for mining', 'Utilities', 'Construction',
                       'Wood products', 'Nonmetallic mineral products', 'Primary metals',
                       'Fabricated metal products', 'Machinery',
                       'Computer and electronic products',
                       'Electrical equipment, appliances, and components',
                       'Motor vehicles, bodies and trailers, and parts',
                       'Other transportation equipment', 'Furniture and related products',
                       'Miscellaneous manufacturing', 'Food and beverage and tobacco products',
                       'Textile mills and textile product mills',
                       'Apparel and leather and allied products', 'Paper products',
                       'Printing and related support activities',
                       'Petroleum and coal products', 'Chemical products',
                       'Plastics and rubber products', 'Wholesale trade',
                       'Motor vehicle and parts dealers', 'Food and beverage stores',
                       'General merchandise stores', 'Other retail', 'Air transportation',
                       'Rail transportation', 'Water transportation', 'Truck transportation',
                       'Transit and ground passenger transportation',
                       'Pipeline transportation',
                       'Other transportation and support activities',
                       'Warehousing and storage',
                       'Publishing industries, except internet (includes software)',
                       'Motion picture and sound recording industries',
                       'Broadcasting and telecommunications',
                       'Data processing, internet publishing, and other information services',
                       'Federal Reserve banks, credit intermediation, and related activities',
                       'Securities, commodity contracts, and investments',
                       'Insurance carriers and related activities',
                       'Funds, trusts, and other financial vehicles', 'Housing',
                       'Other real estate',
                       'Rental and leasing services and lessors of intangible assets',
                       'Legal services', 'Computer systems design and related services',
                       'Miscellaneous professional, scientific, and technical services',
                       'Management of companies and enterprises',
                       'Administrative and support services',
                       'Waste management and remediation services', 'Educational services',
                       'Ambulatory health care services', 'Hospitals',
                       'Nursing and residential care facilities', 'Social assistance',
                       'Performing arts, spectator sports, museums, and related activities',
                       'Amusements, gambling, and recreation industries', 'Accommodation',
                       'Food services and drinking places',
                       'Other services, except government',
                       'Federal general government (defense)',
                       'Federal general government (nondefense)',
                       'Federal government enterprises', 'State and local general government',
                       'State and local government enterprises',
                       'Scrap, used and secondhand goods',
                       'Noncomparable imports and rest-of-the-world adjustment']

        for i in range(len(names)):
            newrec = Legend(name=names[i], index=i, level=level)
            newrec.save()
        # del newrec



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
