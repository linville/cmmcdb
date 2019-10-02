# This exports an OpenXML spreadsheet of the CMMC Model Framework.

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max

from cmmcdb.models import *

import argparse
import json
import datetime


class Command(BaseCommand):
    """ Exports an Open XML"""

    help = "Exports an Open XML format"

    def handle(self, *args, **options):
        from openpyxl import Workbook
        from openpyxl.utils import get_column_letter
        from openpyxl.styles import Alignment, Font, Color, PatternFill

        # from openpyxl.descriptors import Alias

        self.wb = Workbook()
        self.wb_row = 1
        # wb.active

        self.ml = {}
        for ml in MaturityLevel.objects.order_by("level").all():
            self.ml[ml.level] = ml

        # Column Formatting
        self.wb.active.column_dimensions[get_column_letter(1)].width = 45
        for i in range(2, 6):
            self.wb.active.column_dimensions[get_column_letter(i)].width = 40

        # Output Domain
        for domain in Domain.objects.order_by("short").all():
            print(f"Domain: {domain.name}")
            self.wb.active.merge_cells(
                start_row=self.wb_row, start_column=1, end_row=self.wb_row, end_column=6
            )
            c = self.wb.active.cell(
                column=1, row=self.wb_row, value=f"Domain: {domain.name}"
            )
            c.font = Font(size=14, bold=True, color="ffffff")
            c.fill = PatternFill("solid", fgColor="0000ff")

            self.wb_row += 1
            for capability in domain.capabilities.order_by("process", "index").all():
                c = self.wb.active.cell(
                    column=1,
                    row=self.wb_row,
                    value=f"C{capability.index} {capability.name}",
                )
                c.alignment = Alignment(
                    horizontal="general", vertical="top", wrap_text=True
                )

                if capability.process:
                    c.fill = PatternFill("solid", fgColor="ddddff")

                self.wb_row += 1

                self.export_capability(capability)

            print("\n\n\n")
            self.wb_row += 1

        self.wb.save(filename=("cmmc.xlsx"))

    def export_capability(self, capability):
        max_index = capability.activities.aggregate(Max("index"))["index__max"]

        for i in range(1, max_index + 1):
            self.export_capability_row(capability, i)
            self.wb_row += 1

    def export_capability_row(self, capability, row):
        ws = self.wb.active

        capability.activities.filter(index=row)

        # c = ws.cell(1, wb_row, value=capability, name)
        for i in range(1, 6):
            try:
                # print(f"    L{i}-{activity.index}: {activity.name}")
                activity = capability.activities.filter(
                    index=row, maturity_level=self.ml[i]
                ).get()

                c = self.wb.active.cell(
                    column=i + 1,
                    row=self.wb_row,
                    value=f"L{i}-{activity.index} {activity.name}",
                )
                c.alignment = Alignment(
                    horizontal="general", vertical="top", wrap_text=True
                )

            except:
                # print(f"    L{i}")
                pass
