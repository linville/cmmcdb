# This imports the CMMC pdf as distributed by OUSD(A&S).

from django.core.management.base import BaseCommand, CommandError
from django.db.models import IntegerField, Case, Sum, Value, When

from cmmcdb.models import *

import argparse
import camelot
import re
import pprint


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


class Command(BaseCommand):
    help = "Imports the CMMC pdf."

    def add_arguments(self, parser):
        parser.add_argument(
            "FILE", type=argparse.FileType("rb", 0), help="Path to the CMMC pdf."
        )

    def check_db(self):
        expected = 5
        found = MaturityLevel.objects.all().count()
        if expected != found:
            raise CommandError(f"Expected {expected} Maturity Levels. Found {found}.")

        expected = 17
        found = Domain.objects.all().count()
        if expected != found:
            raise CommandError(f"Expected {expected} Domains. Found {found}.")

    def handle(self, *args, **options):
        self.check_db()

        # Capabilities may have two pages of practices and the 2nd page will have
        # an empty cell to (poorly) indicate that the capability was continued on.

        last_capability = None

        for page_index in range(18, 37):
            print(f"Reading CMMC pdf page {page_index}...")
            # Extract the Table Header
            header = camelot.read_pdf(
                options["FILE"].name,
                pages=str(page_index),
                flavor="stream",
                table_areas=["50,561,400,538"],
                suppress_stdout=True,
            )
            domain = self.extract_domain(header[0].data[0][0])

            # Extract the Table
            tables = camelot.read_pdf(options["FILE"].name, pages=str(page_index))

            if tables.n != 1:
                raise CommandError(f"Expected 1 table per page. Found {tables.n}.")

            last_capability = self.extract_table(domain,last_capability, tables[0])

    def extract_table(self, domain, last_capability, table):
        if table.shape[1] != 6:
            raise CommandError(f"Expected table to have 6 columns. Found {table.shape[1]} columns on page {table.page}.")

        if table.shape[0] < 3:
            raise CommandError(f"Expected table to have at least 3 rows. Found {table.shape[0]} rows on page {table.page}.")

        #print(table.data)

        # Row 0: Capability, Practices

        # Row 1: Empty Cell, Level 1 ... Level 5

        # Row 2+: Practices
        # Column 0, Capability or Empty Cell
        # Column 1-5: Practice

        is_process = self.extract_is_process(table.data[0])

        for i in range(2, table.shape[0]):
            print(f" Row {i}")

            # Check for a new capability in first column
            if table.data[i][0]:
                last_capability = self.extract_capability(
                    table.data[i][0], domain, is_process
                )

            # Look through all the columns for practices assuming the column index
            # corresponds to the maturity level.
            for j in range(1, 6):
                try:
                    ml = MaturityLevel.objects.get(level=int(j))
                    self.extract_practice(last_capability, ml, table.data[i][j])
                except MaturityLevel.ObjectDoesNotExist:
                    raise CommandError(f"Couldn't find Maturity Level {matches[0][1]}")
                except:
                    pass

        return last_capability

    def extract_domain(self, domain_text):
        regex = "^DOMAIN:\s*(?P<name>.+)\s*\((?P<short>.+)\)"
        matches = re.search(regex, domain_text, re.IGNORECASE).groupdict()
        if not matches:
            raise CommandError(f"Domain regex failed on: {domain_text}")

        try:
            domain = Domain.objects.filter(short=matches['short']).get()
            return domain
        except:
            raise CommandError(f"Error extracting domain: {domain_text}")

    def extract_is_process(self, row):
        if row[1].lower().startswith("practices"):
            return False
        elif row[1].lower().startswith("processes"):
            return True
        else:
            raise CommandError(f"Unknown practice or process: {row[1]}")

    def extract_capability(self, cell, domain, is_process):
        simple_text = " ".join(cell.split())

        if is_process:
            index = 1
            name = simple_text
        else:
            regex = "^C(?P<index>\d+)\s(?P<name>.*?)(?:\(continued\W?\))?$"
            matches = re.search(regex, simple_text, re.IGNORECASE).groupdict()

            try:
                index = int(matches['index'])
                name = " ".join(matches['name'].split())
            except:
                raise CommandError(f"Error extracting capability: {simple_text}")

        if not name.endswith("."):
            name += "."

        try:
            obj, created = Capability.objects.get_or_create(
                index=index,
                name=name,
                process=is_process,
                domain=domain,
            )

            return obj
        except:
            raise CommandError(f"Capability get or create failed on {index}, {name}, {is_process}")

    def extract_practice(self, capability, ml, cell):
        if not cell:
            return

        simple_text = " ".join(cell.split())

        # Quirks
        #simple_text = remove_prefix(simple_text, "L ")

        sections = simple_text.split("•")

        regex = "^(?P<text_id>(?P<type>P|MP)\d+)\s(?P<name>.*?)$"
        matches = re.search(regex, sections[0], re.IGNORECASE)
        # text_id: Full Id - P001, MP001
        # type: M or MP
        # name: Practice name

        try:
            name = matches['name'].strip()
        except:
            raise CommandError(f"Practice didn't extract:\n  {cell}\n  {sections}\n  {matches}")

        if not name.endswith("."):
            name += "."

        # print(f"i,n,m,c: {matches[0][0]}, {name}, {ml}, {capability}")
        practice, created = Practice.objects.get_or_create(
            text_id=matches['text_id'],
            name=name,
            maturity_level=ml,
            capability=capability,
        )

        for reference in sections[1:]:
            # print(f"  {reference}")
            pass
