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
    base_link='http://web.mta.info/developers/data/nyct/turnstile/turnstile_'
    df = pd.read_csv(base_link+current_date.strftime('%y%m%d')+'.txt')
    total=len(df)
    while(current_date < end_date):
        current_date = current_date+timedelta(days=7)
        link=base_link+current_date.strftime('%y%m%d')+'.txt'
        new_df=pd.read_csv(link)
        total+=len(new_df)
        print link,total
        df=df.append(new_df,ignore_index=True)

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


def add_clean_columns(data):

    """
    Cleans the dataframe
    Adds: 'DAY', 'MONTH', 'TIMEFRAME_ENTRIES', 'TIMEFRAME_EXITS'
    Removes: 'ENTRIES', 'EXITS'
    Filters: Keeps entries and exits only between 0 and 5000
    """

    #rename columns
    data = data.rename(columns = {'EXITS                                                               ':'EXITS'})
    #add columns
    data['DAY'] = data['DATE'].apply(
        lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%w'))
    data['MONTH'] = data['DATE'].apply(
        lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%m'))
    data['TIMEFRAME_ENTRIES'] = data['ENTRIES']-data.groupby(['C/A', 'UNIT', 'SCP', 'STATION'])['ENTRIES'].shift(1)
    data['TIMEFRAME_EXITS'] = data['EXITS']-data.groupby(['C/A', 'UNIT', 'SCP', 'STATION'])['EXITS'].shift(1)
    #drop columns
    data = data.drop('ENTRIES', 1)
    data = data.drop('EXITS', 1)
    #remove NAs
    data.dropna()
    #filter entries/exits
    data = data[(data['TIMEFRAME_ENTRIES'] >= 0) & (data['TIMEFRAME_ENTRIES'] <= 5000)]
    data = data[(data['TIMEFRAME_EXITS'] >= 0) & (data['TIMEFRAME_EXITS'] <= 5000)]
    #create traffic column
    data['TRAFFIC'] = data['TIMEFRAME_ENTRIES'] + data['TIMEFRAME_EXITS']
    data = data.drop('TIMEFRAME_ENTRIES', 1)
    data = data.drop('TIMEFRAME_EXITS', 1)

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

    sum_dict = {key: pd.DataFrame for key in DataFrameDict}

    for key in DataFrameDict:
        shift = (DataFrameDict[key].groupby(
            ['DATE', 'TIME']).aggregate(sum) -
            DataFrameDict[key].groupby(['DATE', 'TIME']).aggregate(sum).shift(1)
            )

        shift = shift[shift < 5000]
        shift = shift[shift >= 0]
        sum_dict[key] = shift


    return sum_dict




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


def obtain_full_data():
    data = get_data_local()
    data = add_Day_Month(data)
    dicts = create_dict_by_STATION(data)

    return dicts


def main():
    data = get_data_local("MTA_DATA.csv")
    data = add_Day_Month(data)
    dicts = create_dict_by_STATION(data)
    print(get_Day_sum(dicts))
    #get_month_sum(dicts)
    #dict_station_time_totals(dicts)

if __name__ == '__main__':
    main()
