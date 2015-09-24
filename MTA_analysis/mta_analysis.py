import pandas as pd

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



def main():
    pass


if __name__ == '__main__':
    main()
