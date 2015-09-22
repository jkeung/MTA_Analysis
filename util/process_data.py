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

def creat_dict_by_STATION(data):
    UniqueNames = data["STATION"].unique()
    DataFrameDict = {elem : pd.DataFrame for elem in UniqueNames}
    for key in DataFrameDict.keys():
        DataFrameDict[key] = data[:][data["C/A"] == key]

    return DataFrameDict

def addDayOfWeek(DataFrameDict):
    """
    Given a dict where keys are the stations and values are panda timeseries
    It will add a column of day of week 0 through 6 with 0 being Sunday
    """
    for key in DataFrameDict:
        DataFrameDict[key]['DAY']=DataFrameDict[key]['DATE'].apply(lambda x: datetime.strptime(x,'%m/%d/%Y').strftime('%w'))

    for key in DataFrameDict:
        DataFrameDict[key]['MONTH']=DataFrameDict[key]['DATE'].apply(lambda x: datetime.strptime(x,'%m/%d/%Y').strftime('%m'))

    return DataFrameDict

def main():
    data = get_data()
    dicts = create_dict_by_STATION(data)
    day_month_dic = add_Day_Month(dicts)

if __name__ == '__main__':
    main()
