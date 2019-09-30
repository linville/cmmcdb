cmmcdb
======

Django ActiveRecord structure to to store the Cybersecurity Model Maturity Certification model framework. Includes various Python utilities for converting the PDF distributed by
OUSD(A&S) into a database and for exporting the database as various other formats.


Requirements
============
* Python 3
* Django, for basic usage and custom format exporting.
* camelot-py, for original conversion of PDF into normalized database structure.


Compiling Gray16Lib
===================
    # For normal usage
    pip install -r requirements.txt
    
    # For pdf conversion only
    pip install -r requirements_pdf.txt
