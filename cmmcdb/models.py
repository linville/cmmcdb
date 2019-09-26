# Defines database models to store the data items defined
# by the CMMC Model Framework.

from django.db import models


class Reference(models.Model):
    """ Reference documentation"""

    name = models.CharField(max_length=256, unique=True)


class MaturityLevel(models.Model):
    """ Maturity of activities (either practices or processes)"""

    level = models.IntegerField()
    practice_name = models.CharField(max_length=64, unique=True)
    process_name = models.CharField(max_length=64, unique=True)


class Domain(models.Model):
    """ Domains"""

    name = models.CharField(max_length=256, unique=True)
    short = models.CharField(max_length=3, unique=True)


class Capability(models.Model):
    """ Capabilities"""

    index = models.IntegerField()
    name = models.CharField(max_length=256, unique=True)
    process = models.BooleanField()


class Activity(models.Model):
    """ Practices or Processes"""

    index = models.IntegerField()
    name = models.CharField(max_length=1024, unique=True)

    maturity_level = models.ForeignKey(MaturityLevel, on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    capability = models.ForeignKey(Capability, on_delete=models.CASCADE)


class ActivityReference(models.Model):
    """ Cross-reference entries from activities to reference documents"""

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)

    section = models.CharField(max_length=64)
