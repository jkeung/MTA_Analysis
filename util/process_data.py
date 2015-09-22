import sys
import time
from datetime import datetime,timedelta

from pprint import pprint
import urllib2
import pandas as pd


def get_data():

    endDate=datetime.strptime('150919','%y%m%d')
    currentDate=datetime.strptime('141025','%y%m%d')
    baseLink='http://web.mta.info/developers/data/nyct/turnstile/turnstile_'
    df=pd.read_csv(baseLink+currentDate.strftime('%y%m%d')+'.txt')
    while(currentDate<endDate):
        currentDate=currentDate+timedelta(days=7)
        df.append(pd.read_csv(baseLink+currentDate.strftime('%y%m%d')+'.txt'))

    df.to_csv("MTA_DATA.csv")

    return df

def get_data_local():

    data = pd.read_csv("MTA_DATA.csv")
    return data

def create_dict_by_STATION(data):
    
    UniqueNames = data["STATION"].unique()
    DataFrameDict = {elem : pd.DataFrame for elem in UniqueNames}
    for key in DataFrameDict.keys():
             DataFrameDict[key] = data[:][data["STATION"] == key]

    return DataFrameDict

def dict_station_time_totals(DataFrameDict):
    
    sum_dict = {key: (DataFrameDict[key].groupby(['DATE','TIME']).aggregate(sum)-DataFrameDict[key].groupby(['DATE','TIME']).aggregate(sum).shift(1)) for key in DataFrameDict}

    return sum_dict


def add_Day_Month(data):
    """
    Given a dict where keys are the stations and values are panda timeseries
    It will add a column of day of week 0 through 6 with 0 being Sunday
    """
    data['DAY'] = data['DATE'].apply(lambda x: datetime.strptime(x,'%m/%d/%Y').strftime('%w'))
    data['MONTH'] = data['DATE'].apply(lambda x: datetime.strptime(x,'%m/%d/%Y').strftime('%m'))

    return data

def obtain_full_data():
    data = get_data_local()
    data = add_Day_Month(data)
    dicts = create_dict_by_STATION(data)

    return day_month_dic

def get_month_sum(DataFrameDict):

    month_dict = {}
    for key in DataFrameDict:
        month_dict[key] = DataFrameDict[key].groupby(['STATION', 'MONTH']).aggregate(sum)

    pprint(month_dict)

def main():
    data = get_data_local()
    data = add_Day_Month(data)
    dicts = create_dict_by_STATION(data)
    get_month_sum(dicts)
    #time_dict = dict_station_time_totals(dicts)
    #print(time_dict)

if __name__ == '__main__':
    main()
