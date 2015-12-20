#!/bin/bash

# get and clean data
python clean_data/clean_util.py

# creates charts
frameworkpython analysis/create_charts.py
