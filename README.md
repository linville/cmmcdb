cmmcdb
======

CMMCDB is a suite of utilities for importing the [Cybersecurity Model Maturity Certification (CMMC) model framework](https://www.acq.osd.mil/cmmc/) into a normalized database structure (i.e.: Django active record model). It includes capabilities for importing the original PDF distributed by OUSD(A&S) and then exporting various other formats including OpenXML and JSON.


Requirements
------------
* [Django](https://www.djangoproject.com), Python app framework used for active record, database abstraction, etc.
* [camelot-py](https://camelot-py.readthedocs.io/en/master/), for parsing the PDF and extraction of tabular data.


Setup Environment
-----------------
    # Get the code
    git clone https://github.com/linville/cmmcdb.git
    cd cmmcdb
    
    # Setup venv and get dependencies
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt


Basic Usage
-----------
    # Create the sqlite database
    ./manage.py migrate
    
    # Setup basic structures (populate domains and maturity levels)
    ./manage.py bootstrap
    
    # Convert the PDF and import it into the database
    ./manage.py importpdf /path/to/cmmc.pdf
    
    # Export to an Microsoft Excel compatible OpenXML document
    ./manage.py exportxlsx
    
    # Export to JSON (formatted as a Django fixture)
    ./manage.py dumpdata --indent 2 cmmcdb
