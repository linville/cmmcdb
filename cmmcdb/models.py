# Defines database models to store the data items defined
# by the CMMC Model Framework.

from django.db import models


class Reference(models.Model):
    """ Reference documentation"""

    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class MaturityLevel(models.Model):
    """ Maturity of activities (either practices or processes)"""

    level = models.IntegerField()
    practice_name = models.CharField(max_length=64, unique=True)
    process_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"Level {self.level}"


class Domain(models.Model):
    """ Domains"""

    name = models.CharField(max_length=256, unique=True)
    short = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return f"{self.name} ({self.short})"


class Capability(models.Model):
    """ Capabilities"""

    index = models.IntegerField()
    name = models.CharField(max_length=256, unique=True)
    process = models.BooleanField()

    domain = models.ForeignKey(
        Domain, on_delete=models.CASCADE, related_name="capabilities"
    )

    def __str__(self):
        return f"C{self.index} {self.name}"


class Practice(models.Model):
    """ Practices (also Processes if parent capability is a Process Maturity)"""

    practice_number = models.IntegerField()
    name = models.CharField(max_length=1024)

    maturity_level = models.ForeignKey(MaturityLevel, on_delete=models.CASCADE)
    capability = models.ForeignKey(
        Capability, on_delete=models.CASCADE, related_name="practices"
    )

    def __str__(self):
        return f"{self.text_id} {self.name}"


class PracticeReference(models.Model):
    """ Cross-reference entries from practices to reference documents"""

    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)

    section = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.practice.name} - {self.reference.name}"
