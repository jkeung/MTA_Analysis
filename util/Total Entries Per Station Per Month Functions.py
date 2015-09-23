

# 2 functions to get entries for stations per month. 

### first function takes a datafile, month, and station and returns the total entries for that month and at that station. 
### second function takes a datafile, month and returns a dictionay where the stations are the keys and the total entries for that station per month are the values. 

###first function
def entries_for_given_month_and_station(data_file, month, station):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import datetime 
    import collections
    from collections import defaultdict
    import dateutil     
    from dateutil import parser
    df = pd.read_csv(data_file)
    sliced_df = df.ix[:,[3,6,9]]
    df_tup = list(sliced_df.itertuples())
    d = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
    for row in df_tup:
        station = row[1]
        entry = row[3]
        da = parser.parse(row[2])
        outerkey = da.month
        if d[outerkey] == 0:
            d[outerkey]={station:entry}
        elif station not in d[outerkey].keys():
            d[outerkey].update({station:entry})
        else:
            d[outerkey][station] += entry
    print d[month][station]

####second function 
def station_entries_for_given_month(data_file, month,):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import datetime 
    import collections
    from collections import defaultdict
    import dateutil     
    from dateutil import parser
    df = pd.read_csv(data_file)
    sliced_df = df.ix[:,[3,6,9]]
    df_tup = list(sliced_df.itertuples())
    d = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
    for row in df_tup:
        station = row[1]
        entry = row[3]
        da = parser.parse(row[2])
        outerkey = da.month
        if d[outerkey] == 0:
            d[outerkey]={station:entry}
        elif station not in d[outerkey].keys():
            d[outerkey].update({station:entry})
        else:
            d[outerkey][station] += entry
    print d[month]

