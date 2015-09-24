
def get_top_hours(data, filename='top_days.png'):

    hours = ["00:00:00", "04:00:00", "08:00:00", "12:00:00", "16:00:00", "20:00:00"]
    data = data[data["TIME"].isin(hours)]
    top_hours = data.groupby(['TIME']).sum()
    ax = top_hours.plot(kind='bar', title='Top Turnstile Traffic for 4 Hour Interval of Day')
    fig = ax.get_figure()
    fig.savefig(filename, bbox_inches='tight')

    return top_hours

def main():
    pass


if __name__ == '__main__':
    main()
