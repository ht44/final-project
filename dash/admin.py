from django.contrib import admin
from .models import SectorUse, SummaryUse, SectorMake, SummaryMake

admin.site.register(SectorUse)
admin.site.register(SummaryUse)
admin.site.register(SectorMake)
admin.site.register(SummaryMake)

# Register your models here.
