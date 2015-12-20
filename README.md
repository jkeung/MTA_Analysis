# MTA Turnstile Analysis
Optimize your street vendor schedules by finding the busiest turnstiles in NYC by month, day of week, or hour.

# Clone the repository

```$ git clone https://github.com/jkeung/MTA_Analysis.git```

## Setup

This code is portable across the following OS's: Linux distributions, Mac and Windows OS's. Scripts were written using Python 2.7 and have not been tested for portability to Python 3.X.

You are encouraged to use a python virtual environment using virtualenv and pip. 

```$ virtualenv mta_analysis```

### Install requirements:

```$ pip install -r requirements.txt```

#### Description of modules imported and application

* cycler - Composable style cycles
* funcsigs - Python function signatures from PEP362 for Python 2.6, 2.7 and 3.2+
* matplotlib - A python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms
* mock - A library for testing in Python
* nose - Extends unittest to make testing easier
* numpy - NumPy is the fundamental package for scientific computing with Python
* pandas - Pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language
* pbr - PBR is a library that injects some useful and sensible default behaviors into your setuptools run
* pyparsing - A Python Parsing Module
* python-dateutil - Extensions to the standard Python datetime module
* pytz - World timezone definitions, modern and historical
* six - Python 2 and 3 compatibility utilities
* wheel - A built-package format for Python.

If there are issues installing matplotlib create this file in <virtualenv_name>/bin/frameworkpython
(http://matplotlib.org/faq/virtualenv_faq.html) 

```
#!/bin/bash

# what real Python executable to use
PYVER=2.7
PATHTOPYTHON=/usr/local/bin/
PYTHON=${PATHTOPYTHON}python${PYVER}

# find the root of the virtualenv, it should be the parent of the dir this script is in
ENV=`$PYTHON -c "import os; print os.path.abspath(os.path.join(os.path.dirname(\"$0\"), '..'))"`

# now run Python with the virtualenv set as Python's HOME
export PYTHONHOME=$ENV
exec $PYTHON "$@"
```

## Run Scraping and Analyzing Script

Application can be run separately or all at once from a shell script.

#### To run separately:

```
# get and clean data
$ python clean_data/clean_util.py

# create charts for analysis
$ frameworkpython analysis/create_charts.py

```

#### To run via shell script:

```$ source mta_analysis.sh```