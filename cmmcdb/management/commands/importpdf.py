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
        return text[len(prefix):]
    return text


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

        if table.shape[0] < 3:
            raise CommandError(f"Expected table to have at least 3 rows. Found {table.shape[0]} rows on page {table.page}.")


        # Row 0: Domain
        
        # Rows 1 and 2 are a bit broken due first cell vertically spanning 2 rows.
        # Row 1: Practices|Processes / Maturity Level Capability|Capability
        # Row 2: Maturity Levels
        
        # Column 0, Row 3: Capability
        # Column 1-5, Row 3+: Activities

        #print(table.data)
        domain = self.extract_domain(table.data[0])
        is_process = self.extract_is_process(table.data[1])
        
        capability = None
        for i in range(3, table.shape[0]):
            print(f"Row {i}")
            if table.data[i][0]:
                capability = self.extract_capability(table.data[i][0], domain, is_process)
            
            for j in range(1, 6):
                try:
                    self.extract_activity(table.data[i][j], capability)
                except:
                    pass
            
    
    def extract_domain(self, row):
        regex = "^DOMAIN:\s*(.+)\s*\((.+)\)"
        matches = re.findall(regex, row[0], re.IGNORECASE)
        
        try:
            domain = Domain.objects.filter(short=matches[0][1]).get()
            return domain
        except:
            raise CommandError(f"Failed to identify domain in text: {row}")

    def extract_is_process(self, row):
        if row[0].lower().startswith("practices"):
            return False
        elif row[0].lower().startswith("processes"):
            return True
        else:
            raise CommandError(f"Unknown practice or process: {row[0]}")
    
    def extract_capability(self, cell, domain, is_process):
        simple_text = " ".join(cell.split())

        if is_process:
            index = 1
            name = simple_text
        else:
            regex = "^C(\d)\s(.*?)(?:\(continued\W?\))?$"
            matches = re.findall(regex, simple_text, re.IGNORECASE)
            # Group 0: Index
            # Group 1: Activity
        
            try:
                index = int(matches[0][0])
                name =  " ".join(matches[0][1].split())
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

    def extract_activity(self, cell, capability):
        if not cell:
            return

        simple_text = " ".join(cell.split())
        
        # Quirks
        simple_text = remove_prefix(simple_text, "L ")
        
        sections = simple_text.split("•")
        
        regex = "^(L|ML)(\d)-(\d)\s(.*?)$"
        matches = re.findall(regex, sections[0], re.IGNORECASE)
        # Group 0: Type (L or ML)
        # Group 1: Maturity Level
        # Group 2: Index
        # Group 3: Activity Name

        try:
            name = matches[0][3].strip()
        except:
            raise CommandError(f"Activity didn't extract:\n  {cell}\n  {sections}\n  {matches}")
            
        if not name.endswith("."):
            name += "."

        try:
            ml = MaturityLevel.objects.get(level=int(matches[0][1]))
        except MaturityLevel.ObjectDoesNotExist:
            raise CommandError(f"Couldn't find Maturity Level {matches[0][1]}")
        
        
        #print(f"n,i,m,c: {name}, {int(matches[0][2])}, {ml}, {capability}")
        activity, created = Activity.objects.get_or_create(
            name=name,
            index=int(matches[0][2]),
            maturity_level=ml,
            capability=capability,
        )
        
        for reference in sections[1:]:
            #print(f"  {reference}")
            pass
