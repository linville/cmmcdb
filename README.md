cmmcdb
======

Django ActiveRecord structure to to store the [Cybersecurity Model Maturity Certification model framework](https://www.acq.osd.mil/cmmc/). Includes various Python utilities for converting the PDF distributed by
OUSD(A&S) into a database and for exporting the database as various other formats.


Requirements
============
* Python 3
* Django, for basic usage and custom format exporting.
* camelot-py, for original conversion of PDF into normalized database structure.


Setup Environment
=================
    # Get the code
    git clone https://github.com/linville/cmmcdb.git
    cd cmmcdb
    
    # Setup venv and get dependencies
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt


Basic Usage
===========
    # Create the sqlite database
    ./manage.py migrate
    
    # Setup basic structures (populate domains and maturity levels)
    ./manage.py bootstrap
    
    # Convert the PDF and import it into the database
    ./manage.py importpdf /path/to/cmmc.pdf
    
    # Export to an Microsoft Excel compatible OpenXML document
    ./manage.py exportxlsx
