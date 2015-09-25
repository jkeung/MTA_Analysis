from datetime import datetime, timedelta

from pprint import pprint
import pandas as pd


def get_data():

    """
    Downloads data from online MTA data source
    It loops through all recent data, and appends it to a single csv datafile
    """

    end_date = datetime.strptime('150919', '%y%m%d')
    current_date = datetime.strptime('141025', '%y%m%d')
    base_link = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_'
    df = pd.read_csv(base_link+current_date.strftime('%y%m%d')+'.txt')
    total = len(df)
    while(current_date < end_date):
        current_date = current_date+timedelta(days=7)
        link = base_link+current_date.strftime('%y%m%d')+'.txt'
        new_df = pd.read_csv(link)
        total += len(new_df)
        print link, total
        df = df.append(new_df, ignore_index=True)

    return df


def save_file(name, data):

    """
    Saves pandas data to a csv file
    """

    data.to_pickle(name)


def get_data_local(name):

    """
    Reads data from local csv file
    """

    data = pd.read_pickle(name)
    return data


def add_clean_columns(data):

    """
    Cleans the dataframe
    Adds: 'DAY', 'MONTH', 'TIMEFRAME_ENTRIES', 'TIMEFRAME_EXITS'
    Removes: 'ENTRIES', 'EXITS'
    Filters: Keeps entries and exits only between 0 and 5000

    ORDER MATTERS FOR CLEANING
    """

    data = data.rename(columns={'EXITS                                                               ': 'EXITS'})
    data = add_day_month(data)
    data = add_entry_exit_totals(data)
    data = drop_unneeded_columns(data)
    data = add_traffic_column(data)
    data = add_time_bin_column(data)

    return data


def add_time_bin_column(data):

    """
    Takes a dataframe and creates a column with the times binned by every 4 hours
    """

    data["TIME_INT"] = data["TIME"].map(lambda x: int(x.replace(":", "")))
    data["TIME_BIN"] = data["TIME_INT"].map(lambda x: get_range(x))
    data = data.drop("TIME_INT", 1)

    return data


def get_range(time):

    """
    used in add_time_bin to get the correct bin for the TIME_BIN column
    """

    hours = [0, 40000, 80000, 120000, 160000, 200000]
    curr = 0
    prev = 0
    for h in hours:
        curr = h
        if time <= curr and time > prev:
            return float(curr/10000)
        elif time == 200000:
            float(200000/10000)
            return float(200000/10000)
        elif time > float(200000):
            return float(24)
        elif time == 0:
            return float(24)


def add_traffic_column(data):

    """
    Given a DatraFrame it addes a column
    that is the sum of the Entries and Exits for a station
    """

    data = data[(data['TIMEFRAME_ENTRIES'] >= 0) &
                (data['TIMEFRAME_ENTRIES'] <= 5000)]
    data = data[(data['TIMEFRAME_EXITS'] >= 0) &
                (data['TIMEFRAME_EXITS'] <= 5000)]
    data['TRAFFIC'] = data['TIMEFRAME_ENTRIES'] + data['TIMEFRAME_EXITS']
    data = data.drop('TIMEFRAME_ENTRIES', 1)
    data = data.drop('TIMEFRAME_EXITS', 1)

    return data


def drop_unneeded_columns(data):

    """
    removes the ENTRIES and EXITS column
    and also drops na values
    """

    data = data.drop('ENTRIES', 1)
    data = data.drop('EXITS', 1)
    data.dropna()

    return data


def add_entry_exit_totals(data):

    """"
    Given a DataFrame it creates two columns containing both the
    sum of ENTRIES and EXITS
    """


    entries = data['ENTRIES'] - \
        data.groupby(['C/A', 'UNIT', 'SCP', 'STATION'])['ENTRIES'].shift(1)
    exit = data['EXITS'] - \
        data.groupby(['C/A', 'UNIT', 'SCP', 'STATION'])['EXITS'].shift(1)

    data['TIMEFRAME_ENTRIES'] = entries
    data['TIMEFRAME_EXITS'] = exit

    return data


def add_day_month(data):

    """
    Given a DataFrame it creates columns for the Day, Day int value, 
    and the Month
    """

    data['DAY'] = data['DATE'].apply(
        lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%a'))
    data['DAY_NUM'] = data['DATE'].apply(
        lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%w'))
    data['MONTH'] = data['DATE'].apply(
        lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%m'))

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


def get_Day_sum(DataFrameDict):

    """"
    This takes a dictionary of data frames
    Returns a dictionary of dataframes containing the sum of entries per day
    For the given station as a key
    """

    day_dict = {}
    for key in DataFrameDict:
        day_dict[key] = DataFrameDict[key].groupby(
            ['STATION', 'DAY']).aggregate(sum)

    print(day_dict)

    return day_dict


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

    return month_dict


def get_hour_sum(DataFrameDict):
    
    """"
    This takes a dictionary of data frames
    Returns a dictionary of dataframes containing the sum of entries per month
    For the given station as a key
    """

    hour_dict = {}
    for key in DataFrameDict:
        hour_dict[key] = DataFrameDict[key].groupby(
            ['STATION', 'TIME']).aggregate(sum)

    return hour_dict


def main():
    data = get_data()
    save_file("MTA_DATA.p",data)


if __name__ == '__main__':
    main()
