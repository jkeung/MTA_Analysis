from datetime import datetime, timedelta

from pprint import pprint
import pandas as pd


def get_data():
    """
    Downloads data from online MTA data source
    It loops through all recent data, and appends it to a single csv datafile
    """

    endDate = datetime.strptime('150919', '%y%m%d')
    currentDate = datetime.strptime('141025', '%y%m%d')
    baseLink = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_'
    df = pd.read_csv(baseLink+currentDate.strftime('%y%m%d')+'.txt')
    while(currentDate < endDate):
        currentDate = currentDate+timedelta(days=7)
        df.append(pd.read_csv(baseLink+currentDate.strftime('%y%m%d')+'.txt'))

    return df


def save_file(name, data):

    """
    Saves pandas data to a csv file
    """

    data.to_csv(name)


def get_data_local(name):
    """
    Reads data from local csv file
    """

    data = pd.read_csv(name)
    return data


def create_dict_by_STATION(data):

    """
    This converts the MTA data frame into a dictionary
    The stations are keys
    The values are data frames
    The data frames are the data that has the key in the stations column
    """

    UniqueNames = data["STATION"].unique()
    DataFrameDict = {elem: pd.DataFrame for elem in UniqueNames}
    for key in DataFrameDict.keys():
        DataFrameDict[key] = data[:][data["STATION"] == key]

    return DataFrameDict


def dict_station_time_totals(DataFrameDict):

    """
    Takes a dictionary of dataframes
    Returns a data frame containing
    the difference in entries per station from one time frame to the next
    """

    sum_dict = {key: (DataFrameDict[key].groupby(
        ['DATE', 'TIME']).aggregate(sum) -
        DataFrameDict[key].groupby(['DATE', 'TIME']).aggregate(sum).shift(1))
        for key in DataFrameDict}

    return sum_dict


def add_Day_Month(data):

    """
    Given a dict where keys are the stations and values are panda timeseries
    It will add a column of day of week 0 through 6 with 0 being Sunday
    """

    data['DAY'] = data['DATE'].apply(
        lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%w'))
    data['MONTH'] = data['DATE'].apply(
        lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%m'))

    return data


def get_month_sum(DataFrameDict):
    """"
    This takes a dictionary of data frames
    Returns a dictionary of dataframes containing the sum of entries per month
    For the given station as a key
    """

    month_dict = {}
    for key in DataFrameDict:
        month_dict[key] = DataFrameDict[key].groupby(
            ['STATION', 'MONTH']).aggregate(sum)

    pprint(month_dict)


def obtain_full_data():
    data = get_data_local()
    data = add_Day_Month(data)
    dicts = create_dict_by_STATION(data)

    return dicts


def main():
    data = get_data_local("MTA_DATA.csv")
    save_file("MTA_DATA.csv", data)
    data = add_Day_Month(data)
    dicts = create_dict_by_STATION(data)
    get_month_sum(dicts)
    dict_station_time_totals(dicts)

if __name__ == '__main__':
    main()
