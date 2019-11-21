# Test various PDF importing methods

from django.test import TestCase

from cmmcdb.models import *
from cmmcdb.management.commands import importpdf


class TestImport(TestCase):
    """Tests for PDF importing"""

    def setUp(self):
        self.cmd = importpdf.Command()

        self.domain = Domain.objects.create(name="Access Control", short="AC")
        self.capability = Capability.objects.create(
            index=1, name="Testing 1 2 3.", process=False, domain=self.domain
        )

    def test_extract_domain(self):
        check_domain = self.cmd.extract_domain("DOMAIN: ACCESS CONTROL (AC)")

        self.assertEqual(self.domain, check_domain)

    def test_extract_capability(self):
        check_cap = self.cmd.extract_capability(
            "C001\nTesting 1 2 3", self.domain, False
        )

        self.assertEqual(self.capability, check_cap)
