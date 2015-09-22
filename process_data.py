import sys
from datetime import datetime,timedelta

import urllib2
import pandas as pd


def get_data():
    endDate=datetime.strptime('150919','%y%m%d')
    currentDate=datetime.strptime('141019','%y%m%d')
    baseLink='http://web.mta.info/developers/data/nyct/turnstile/turnstile_'

    df=pd.read_csv(baseLink+currentDate.strftime('%y%m%d')+'.txt')
    while(currentDate<endDate):
        currentDate=currentDate+timedelta(days=7)
        print currentDate
        df.append(pd.read_csv(baseLink+currentDate.strftime('%y%m%d')+'.txt'))

    return df

def main():
    data = get_data()

if __name__ == '__main__':
    main()
