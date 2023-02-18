from django.db import models

class VSPOMs(models.Model)
    dispersal_kernel = models.IntegerField()
    connectivity = models.IntegerField()
    colonization = models.IntegerField()
    extinction = models.IntegerField()
    extinction_rescue = models.IntegerField
    stochasticity = models.IntegerField()
