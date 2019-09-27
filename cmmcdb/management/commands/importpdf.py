# This imports the CMMC pdf as distributed by OUSD(A&S).

from django.core.management.base import BaseCommand, CommandError
from django.db.models import IntegerField, Case, Sum, Value, When

from cmmcdb.models import *

import argparse
import camelot


class Command(BaseCommand):
    help = "Imports the CMMC pdf."

    def add_arguments(self, parser):
        parser.add_argument('FILE', type=argparse.FileType('rb', 0), help = "Path to the CMMC pdf.")

    def check_db(self):
        expected = 5
        found = MaturityLevel.objects.all().count()
        if expected != found:
            raise CommandError(f"Expected {expected} Maturity Levels. Found {found}.")
        
        expected = 18
        found = Domain.objects.all().count()
        if expected != found:
            raise CommandError(f"Expected {expected} Domains. Found {found}.")

    def handle(self, *args, **options):
        self.check_db()
        
        for page_index in range(3, 58):
            print(f"Reading CMMC pdf page {page_index}...")
            tables = camelot.read_pdf(options["FILE"].name, pages=str(page_index))
            
            if tables.n != 1:
                raise CommandError(f"Expected 1 table per page. Found {tables.n}.")
            
            self.extract_table(tables[0])
    
    def extract_table(self, table):
        if table.shape[1] != 6:
            raise CommandError(f"Expected table to have 6 columns. Found {table.shape[1]} columns on page {table.page}.")

        # Row 0: Domain
        
        # Rows 1 and 2 are a bit broken due first cell vertically spanning 2 rows.
        # Row 1: Practices|Processes / Maturity Level Capability|Capability
        # Row 2: Maturity Levels
        
        # Column 0, Row 3: Capabilities
        # Column 1-5, Row 3+: Activities
        print(table.data)
        