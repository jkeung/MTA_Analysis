
def get_top_hours(data, filename='top_hours.png'):

    """
    Given a Processed DataFrame it plots the hours in a day binned by 4 hours
    """

    top_hours = data.groupby(['TIME_BIN']).sum()
    ax = top_hours.plot(kind='bar', title='Top Turnstile Traffic for 4 Hour Interval of Day')
    fig = ax.get_figure()
    fig.savefig(filename, bbox_inches='tight')

    return top_hours


def get_top_n_stations(data, n, filename='top_stations.png'):
    """
    Given dataframe containing cleaned data, identifies top n stations
    and saves plot of distribution.
    """
    top_stations = data.groupby(['STATION']).sum().sort('TRAFFIC', ascending=False).head(n)
    ax = top_stations[['TRAFFIC']].plot(kind='bar', title='Top %s Stations Turnstile Traffic ' % n)
    fig = ax.get_figure()
    fig.savefig(filename, bbox_inches='tight')

    return top_stations[['TRAFFIC']]


def get_top_days(data, filename='top_days.png'):

    """
    Given dataframe containing cleaned data, identifies sums of all data by days.
    """

    top_days = data.groupby(['DAY_NUM', 'DAY']).sum()
    ax = top_days[['TRAFFIC']].plot(kind='bar', title='Top Turnstile Traffic for Day of Week')
    fig = ax.get_figure()
    fig.savefig(filename, bbox_inches='tight')

    return top_days[['TRAFFIC']]

def get_month_sums(data, filename = 'month_sums.png'):

    """
    Given dataframe containing cleaned data, identifies sums of all data by month and saves plot.
    """

    months = data[(data['MONTH']!='09') & (data['MONTH']!='10')].groupby('MONTH').sum()
    ax = months[['TRAFFIC']].plot(kind='bar',title='Sum Of Months')
    fig = ax.get_figure()
    fig.savefig(filename, bbox_inches='tight')

    return months[['TRAFFIC']]

def plot_station(data, station):

    """
    Given dataframe containing cleaned data and list of stations, plots time bin data 
    for a station
    """
    topstationdata = data[data['STATION']==station]
    ax = topstationdata.groupby(['TIME_BIN']).sum().plot(kind = 'bar', title='%s Station Schedule' % station)
    fig = ax.get_figure()
    fig.savefig('%s_station_schedule.png' %station.replace(' ', '_'), bbox_inches='tight')
    
    return topstationdata


def plot_station(data, station):

    """
    Given dataframe containing cleaned data and list of stations, plots time bin data 
    for a station
    """
    topstationdata = data[data['STATION']==station]
    ax = topstationdata.groupby(['TIME_BIN']).sum().plot(kind = 'bar', title='%s Station Schedule' % station)
    fig = ax.get_figure()
    fig.savefig('%s_station_schedule.png' %station.replace(' ', '_'), bbox_inches='tight')
    
    return topstationdata
 

defmain():
    pass


if __name__ == '__main__':
    main()
