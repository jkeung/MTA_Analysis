
<<<<<<< HEAD
def get_top_hours(data, filename='top_days.png'):

    hours = ["00:00:00", "04:00:00", "08:00:00", "12:00:00", "16:00:00", "20:00:00"]
    data = data[data["TIME"].isin(hours)]
    top_hours = data.groupby(['TIME']).sum()
    ax = top_hours.plot(kind='bar', title='Top Turnstile Traffic for 4 Hour Interval of Day')
    fig = ax.get_figure()
    fig.savefig(filename, bbox_inches='tight')

    return top_hours
=======
def get_top_n_stations(data, n, filename='top_stations.png'):
    """
    Given dataframe containing cleaned data, identifies top n stations
    and saves plot of distribution.
    """
    top_stations = data.groupby(['STATION']).sum().sort('TRAFFIC', ascending = False).head(n)
    ax = top_stations.plot(kind = 'bar', title = 'Top %s Stations Turnstile Traffic ' % n)
    fig = ax.get_figure()
    fig.savefig(filename, bbox_inches='tight')
    
    return top_stations

def get_top_days(data, filename = 'top_days.png'):
    
    top_days = data.groupby(['DAY_NUM', 'DAY']).sum()
    ax = top_days.plot(kind = 'bar', title = 'Top Turnstile Traffic for Day of Week')
    fig = ax.get_figure()
    fig.savefig(filename, bbox_inches='tight')

    return top_days


>>>>>>> aec72a8d354438762082ec014b7343abfae66702

def main():
    pass


if __name__ == '__main__':
    main()
