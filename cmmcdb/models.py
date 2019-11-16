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
    
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='capabilities')


class Practice(models.Model):
    """ Practices (also Processes if parent capability is a Process Maturity)"""

    text_id = models.CharField(max_length=8)
    name = models.CharField(max_length=1024)

    maturity_level = models.ForeignKey(MaturityLevel, on_delete=models.CASCADE)
    capability = models.ForeignKey(Capability, on_delete=models.CASCADE, related_name='practices')


class PracticeReference(models.Model):
    """ Cross-reference entries from practices to reference documents"""

    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)

    section = models.CharField(max_length=64)
