# The bootstrap command is a manual insertion of a small portion of
# the 0.6b draft release of the CMMC Model Framework. The bootstrap
# is used for preliminary developing and testing changes in the
# structure of the database model.

from django.core.management.base import BaseCommand, CommandError
from django.db.models import IntegerField, Case, Sum, Value, When

from cmmcdb.models import *

import argparse
import json


class Command(BaseCommand):
    help = """Basic bootstrapping code for high level data. Useful to make the
    PDF import algorithms a little bit easier."""

    def handle(self, *args, **options):
        self.cis = Reference.objects.create(name="CIS")
        self.csf = Reference.objects.create(name="CSF")
        self.dib = Reference.objects.create(name="DIB")
        self.nist = Reference.objects.create(name="NIST SP 800-171")

        self.m1 = MaturityLevel.objects.create(
            level=1,
            practice_name="Basic Cyber Hygiene",
            process_name="Performed"
        )

        self.m2 = MaturityLevel.objects.create(
            level=2,
            practice_name="Intermediate Cyber Hygiene",
            process_name="Documented",
        )

        self.m3 = MaturityLevel.objects.create(
            level=3,
            practice_name="Good Cyber Hygiene",
            process_name="Managed"
        )

        self.m4 = MaturityLevel.objects.create(
            level=4,
            practice_name="Proactive",
            process_name="Reviewed"
        )

        self.m5 = MaturityLevel.objects.create(
            level=5,
            practice_name="Advanced / Progressive",
            process_name="Optimized"
        )

        self.domainAC = Domain.objects.create(short="AC", name="Access Control")
        self.domainAM = Domain.objects.create(short="AM", name="Asset Management")
        self.domainAA = Domain.objects.create(short="AA", name="Audit and Accountability")
        self.domainAT = Domain.objects.create(short="AT", name="Awareness and Training")
        self.domainCM = Domain.objects.create(short="CM", name="Configuration Management")
        self.domainIDA = Domain.objects.create(short="IDA", name="Identification and Authentication")
        self.domainIR = Domain.objects.create(short="IR", name="Incident Response")
        self.domainMA = Domain.objects.create(short="MA", name="Maintenance")
        self.domainMP = Domain.objects.create(short="MP", name="Media Protection")
        self.domainPS = Domain.objects.create(short="PS", name="Personnel Security")
        self.domainPP = Domain.objects.create(short="PP", name="Physical Protection")
        self.domainRE = Domain.objects.create(short="RE", name="Recovery")
        self.domainRM = Domain.objects.create(short="RM", name="Risk Management")
        self.domainSAS = Domain.objects.create(short="SAS", name="Security Assessment")
        self.domainSA = Domain.objects.create(short="SA", name="Situational Awareness")
        self.domainSCP = Domain.objects.create(short="SCP", name="System and Communications Protection")
        self.domainSII = Domain.objects.create(short="SII", name="System and Information Integrity")
