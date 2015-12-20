#!/usr/bin/env python
from datetime import datetime, timedelta
import pandas as pd
import time

OUTFILE = 'MTA_DATA.p'


def get_data():

    """Downloads data from online MTA data source
    Loops through all recent data, and appends it to a single csv datafile

    Ex. http://web.mta.info/developers/data/nyct/turnstile/turnstile_150919.txt
    Args:
        None
    Returns:
        None
    """

    end_date = datetime.strptime(time.strftime("%y%m%d"), '%y%m%d')
    begin_date = datetime.strptime('141025', '%y%m%d')
    base_link = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_'

    while(begin_date < end_date):

        link = '{0}{1}.txt'.format(base_link, begin_date.strftime("%y%m%d"))
        print 'Retrieving data from {0}...'.format(link)
        try:
            new_df = pd.read_csv(link)
            df = df.append(new_df, ignore_index=True)
        except:
            df = pd.read_csv(link)
        begin_date = begin_date + timedelta(days=7)

    return df


def add_clean_columns(df):

    """Cleans the dataframe
    Adds: 'DAY', 'MONTH', 'TIMEFRAME_ENTRIES', 'TIMEFRAME_EXITS'
    Removes: 'ENTRIES', 'EXITS'
    Filters: Keeps entries and exits only between 0 and 5000

    ORDER MATTERS FOR CLEANING

    Args:
        df (pandas.DataFrame): The uncleaned pandas dataframe
    Returns:
        df (pandas.DataFrame): The cleaned pandas dataframe
    """

    df = df.rename(columns={'EXITS                                                               ': 'EXITS'})
    df = add_day_month(df)
    df = add_entry_exit_totals(df)
    df = add_traffic_column(df)
    df = add_time_bin_column(df)

    return df


def add_day_month(df):

    """Creates columns for the Day, Day int value, and the Month

    Args:
        df (pandas.DataFrame): The original pandas dataframe
    Returns:
        df (pandas.DataFrame): The pandas dataframe with the DAY, DAY_NUM, and MONTH columns
    """

    df['DAY'] = df['DATE'].apply(
        lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%a'))
    df['DAY_NUM'] = df['DATE'].apply(
        lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%w'))
    df['MONTH'] = df['DATE'].apply(
        lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%m'))

    return df


def add_entry_exit_totals(df):

    """Creates two columns containing both the sum of ENTRIES and EXITS

    Args:
        df (pandas.DataFrame): The original pandas dataframe
    Returns:
        df (pandas.DataFrame): The pandas dataframe with the TIMEFRAME_ENTRIES and TIMEFRAME_EXITS columns
                               and drops the ENTRIES and EXITS columns
    """

    entries = df['ENTRIES'] - \
        df.groupby(['C/A', 'UNIT', 'SCP', 'STATION'])['ENTRIES'].shift(1)
    exit = df['EXITS'] - \
        df.groupby(['C/A', 'UNIT', 'SCP', 'STATION'])['EXITS'].shift(1)

    df['TIMEFRAME_ENTRIES'] = entries
    df['TIMEFRAME_EXITS'] = exit
    df = df.drop('ENTRIES', 1)
    df = df.drop('EXITS', 1)
    df.dropna()

    return df


def add_traffic_column(df):

    """Add a TRAFFIC column that is the sum of the Entries and Exits for a station

    Args:
        df (pandas.DataFrame): The original pandas dataframe
    Returns:
        df (pandas.DataFrame): The pandas dataframe with the TRAFFIC column and TIMEFRAME_ENTRIES
                               and TIMEFRAME_EXITS columns removed
    """

    df = df[(df['TIMEFRAME_ENTRIES'] >= 0) &
            (df['TIMEFRAME_ENTRIES'] <= 5000)]
    df = df[(df['TIMEFRAME_EXITS'] >= 0) &
            (df['TIMEFRAME_EXITS'] <= 5000)]
    df['TRAFFIC'] = df['TIMEFRAME_ENTRIES'] + df['TIMEFRAME_EXITS']
    df = df.drop('TIMEFRAME_ENTRIES', 1)
    df = df.drop('TIMEFRAME_EXITS', 1)

    return df


def add_time_bin_column(df):

    """
    Takes a dataframe and creates a column with the times binned by every 4 hours

    Args:
        df (pandas.DataFrame): The original pandas dataframe
    Returns:
        df (pandas.DataFrame): The pandas dataframe with the TIME_BIN column
    """

    df["TIME_INT"] = df["TIME"].map(lambda x: int(x.replace(":", "")))
    df["TIME_BIN"] = df["TIME_INT"].map(lambda x: get_range(x))
    df = df.drop("TIME_INT", 1)

    return df


def get_range(time):

    """An function used to get the correct 4 hour interval for the TIME_BIN column

    Takes a dataframe and creates a column with the times binned by every 4 hours

    Args:
        time (int): A time int representation in the format hhmmss
        Ex: noon would be represented as 120000
    Returns:
        output (float): The 4 hour time interval that the integer input time belongs to

    """

    hours = [0, 40000, 80000, 120000, 160000, 200000]
    prev = 0
    output = 0.0
    for h in hours:
        if time <= h and time > prev:
            output = float(h/10000)
            return output
        elif time == 200000:
            output = float(200000/10000)
            return output
        elif time > float(200000):
            output = float(24)
            return output
        # midnight
        elif time == 0:
            output = float(24)
    return output


def main():
    print "Pulling data..."
    df = get_data()
    df = add_clean_columns(df)
    df.to_pickle(OUTFILE)
    print "Pulling data complete!"
    print "Data saved to {0}".format(OUTFILE)

if __name__ == '__main__':
    main()
