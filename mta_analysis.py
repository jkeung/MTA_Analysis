#!/usr/bin/env python
from clean_data import clean_util
from analysis import create_charts

def main():
	clean_util.main()
	create_charts.main()

if __name__ == "__main__":
	main()
