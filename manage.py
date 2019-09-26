#!/usr/bin/env python

# All-in-one Django manage.py to set the configuration of cmmcdb
# to use a local sqlite database.

import os
import sys
import django
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    },
    INSTALLED_APPS=["cmmcdb"],
)

django.setup()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
