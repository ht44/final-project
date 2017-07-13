from django.db import models

# Create your models here.

class Legend(models.Model):
    name = models.CharField(max_length=80)
    level = models.CharField(max_length=30)
    index = models.IntegerField()
    def __str__(self):
        return str(self.val)


class SectorUse(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)

class SectorMake(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)

class SummaryUse(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)

class SummaryMake(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)

class SectorValue(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)

class SummaryValue(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)

class SectorIndustry(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)

class SummaryIndustry(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)

class SectorCommodity(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)

class SummaryCommodity(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)

class SectorDemand(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)

class SummaryDemand(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)

class SectorNoncomp(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)

class SummaryNoncomp(models.Model):
    col = models.IntegerField()
    row = models.IntegerField()
    val = models.DecimalField(max_digits=19, decimal_places=10)
    year = models.IntegerField()
    def __str__(self):
        return str(self.val)
