#!/usr/bin/env python
import os

OUTPUTDIR = 'charts'

def create_dir(directory):

    """Creates directory if doesn't exist
    Args:
        directory: Name of the output directory
    Returns:
        None
    """

    #Check to see if directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_top_hours(df, filename='top_hours.png'):

    """Given a Processed DataFrame this function plots the hours in a day 
    binned by 4 hour time interval and saves a plot of the distribution.

    Args:
        df (pandas.DataFrame): The pandas dataframe that contains the cleaned MTA_data
        filename (str): The output file name for the chart
    Returns:
        top_hours: A pandas series that contains the turnstile traffic by hour.
    """

    outputdir = os.path.join(OUTPUTDIR, 'general')
    create_dir(outputdir)
    output_file = os.path.join(outputdir, filename)
    top_hours = df.groupby(['TIME_BIN']).sum()
    ax = top_hours.plot(kind='bar', title='Top Turnstile Traffic for 4 Hour Interval of Day')
    fig = ax.get_figure()
    fig.savefig(output_file, bbox_inches='tight')

    return top_hours


def get_top_n_stations(df, n, filename='top_stations.png'):
    
    """Given a Processed DataFrame this function identifies the top n
    stations and save a plot of the distribution.

    Args:
        df (pandas.DataFrame): The pandas dataframe that contains the cleaned MTA_data
        n (int): The top number of stations that will be returned.
        filename (str): The output file name for the chart
    Returns:
        top_hours: A pandas series that contains the top n stations.
    """

    outputdir = os.path.join(OUTPUTDIR, 'general')
    create_dir(outputdir)
    output_file = os.path.join(outputdir, filename)
    top_stations = df.groupby(['STATION']).sum().sort_values(by='TRAFFIC', ascending=False).head(n)
    ax = top_stations[['TRAFFIC']].plot(kind='bar', title='Top %s Stations Turnstile Traffic ' % n)
    fig = ax.get_figure()
    fig.savefig(output_file, bbox_inches='tight')

    return top_stations[['TRAFFIC']]


def get_top_days(df, filename='top_days.png'):

    """Given a Processed DataFrame this function aggregates the turnstile
    traffic data by day and saves a plot of the distribution.

    Args:
        df (pandas.DataFrame): The pandas dataframe that contains the cleaned MTA_data
        filename (str): The output file name for the chart
    Returns:
        top_days: A pandas series that contains the turnstile traffic by day of week.
    """

    outputdir = os.path.join(OUTPUTDIR, 'general')
    create_dir(outputdir)
    output_file = os.path.join(outputdir, filename)
    top_days = df.groupby(['DAY_NUM', 'DAY']).sum()
    ax = top_days[['TRAFFIC']].plot(kind='bar', title='Top Turnstile Traffic for Day of Week')
    fig = ax.get_figure()
    fig.savefig(output_file, bbox_inches='tight')

    return top_days[['TRAFFIC']]

def get_month_sums(df, filename = 'month_sums.png'):

    """Given a Processed DataFrame this function aggregates the turnstile
    traffic data by month and saves a plot of the distribution.

    Args:
        data (pandas.DataFrame): The pandas dataframe that contains the cleaned MTA_data
        filename (str): The output file name for the chart
    Returns:
        months (pandas.Series): A pandas series that contains the turnstile traffic by month.
    """

    outputdir = os.path.join(OUTPUTDIR, 'general')
    create_dir(outputdir)
    output_file = os.path.join(outputdir, filename)
    months = df[(df['MONTH']!='09') & (df['MONTH']!='10')].groupby('MONTH').sum()
    ax = months[['TRAFFIC']].plot(kind='bar',title='Sum Of Months')
    fig = ax.get_figure()
    fig.savefig(output_file, bbox_inches='tight')

    return months[['TRAFFIC']]


def plot_station_hour(df, station):

    """Given a Processed DataFrame this function plots the turnstile
    traffic data by hourly time bin for a particular station.

    Args:
        data (pandas.DataFrame): The pandas dataframe that contains the cleaned MTA_data
        station (str): The station name
    Returns:
        top_station_data (pandas.DataFrame): A pandas dataframe that contains the turnstile traffic 
        by hourly time bin.
    """

    outputdir = os.path.join(OUTPUTDIR, 'station_per_hour')
    create_dir(outputdir)
    output_file = os.path.join(outputdir, '%s_hour.png' % station.replace(' ', '_').replace('/', '_'))

    top_station_data = df[df['STATION'] == station]
    hours = top_station_data.groupby(['TIME_BIN']).sum()
    ax = hours.plot(kind='bar', title='%s Station Schedule' % station)
    fig = ax.get_figure()
    fig.savefig(output_file, bbox_inches='tight')

    return top_station_data


def plot_station_day_of_week(df, station):

    """Given a Processed DataFrame this function plots the turnstile
    traffic data by day for a particular station.

    Args:
        data (pandas.DataFrame): The pandas dataframe that contains the cleaned MTA_data
        station (str): The station name
    Returns:
        top_station_data (pandas.DataFrame): A pandas dataframe that contains the turnstile traffic 
        by day.
    """

    outputdir = os.path.join(OUTPUTDIR, 'station_per_day_of_week')
    create_dir(outputdir)
    output_file = os.path.join(outputdir, '%s_station_day_of_week.png' % station.replace(' ', '_').replace('/', '_'))

    top_station_data = df[df['STATION'] == station]
    sums_ = top_station_data.groupby(['DAY']).sum()
    ax = sums_[["TRAFFIC"]].plot(kind='bar', title='%s Station Schedule' % station)
    fig = ax.get_figure()
    fig.savefig(output_file, bbox_inches='tight')

    return top_station_data[['TRAFFIC']]


def plot_station_month(df, station):

    """Given a Processed DataFrame this function plots the turnstile
    traffic data by month for a particular station.

    Args:
        data (pandas.DataFrame): The pandas dataframe that contains the cleaned MTA_data
        station (str): The station name
    Returns:
        top_station_data (pandas.DataFrame): A pandas dataframe that contains the turnstile traffic 
        by month.
    """

    outputdir = os.path.join(OUTPUTDIR, 'station_per_month')
    create_dir(outputdir)
    output_file = os.path.join(outputdir, '%s_month.png' % station.replace(' ', '_').replace('/', '_'))

    top_station_data = df[df['STATION'] == station]
    sums_ = top_station_data.groupby(['MONTH']).sum()
    ax = sums_[["TRAFFIC"]].plot(kind='bar', title='%s Station Schedule' % station)
    fig = ax.get_figure()
    fig.savefig(output_file, bbox_inches='tight')

    return top_station_data[['TRAFFIC']]


def main():
    # Create output directory
    create_dir(OUTPUTDIR)

    # Get list of top 400 stations and save output into output directory
    stations = get_top_n_stations(df, 400).index
    for station in stations:
        plot_station_hour(df, station)
        plot_station_day_of_week(df, station)
        plot_station_month(df, station)

if __name__ == '__main__':
    main()
