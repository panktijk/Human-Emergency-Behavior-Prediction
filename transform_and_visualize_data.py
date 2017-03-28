import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from datetime import datetime

def epoch_to_datetime(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
    
def read_and_transform_data():
    col_names = ['Cab_ID', 'Latitude', 'Longitude', 'Whether_Occupied', 'Timestamp']
    cabs_df = pd.read_csv('Datasets\\cabsdata.csv', names = col_names)
    cabs_df['Timestamp'] = cabs_df['Timestamp'].apply(lambda epoch: epoch_to_datetime(epoch))
    earthquakes_df = pd.read_csv('Datasets\\Earthquakes\\nc_earthquakes.csv')
    earthquakes_df = earthquakes_df[(earthquakes_df['longitude'] <= -122) & (earthquakes_df['place'].str.contains('San Francisco')) & (earthquakes_df['mag'] >= 2)]
    return cabs_df, earthquakes_df

def trace_trajectory(df_temp, m):
    lat = df_temp.Latitude.values
    lon = df_temp.Longitude.values
    x, y = m(lon, lat)
    m.plot(x, y, 'o', markersize=5)
    #plt.plot(x, y, '-', color=np.random.rand(3,))
    plt.plot(x, y, '-', color='yellow')
    
def get_continuous_paths(df):
    splits = np.append(np.where(np.diff(df['Whether_Occupied']) != 0)[0], len(df)+1)+1
    prev = 0
    paths_df = []
    for split in splits:
        paths_df += [df[prev:split]]
        prev = split
    return paths_df
    
def visualize(df):
    paths_df = get_continuous_paths(df)
    m = Basemap(llcrnrlon=-122.56,llcrnrlat=37.4,urcrnrlon=-122,urcrnrlat=37.99, epsg=4269)
    #df1 = df.iloc[7797212:7797220]
    for path_df in paths_df[:10]:
        #if (1 in path_df['Whether_Occupied']):
            trace_trajectory(path_df, m)   
    #df2 = df.iloc[356768:356781]
    #trace_trajectory(df2, m)
    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 2500, verbose= True)
    plt.show()
    
def get_earthquake_dates_and_locs(df):
    dates = [t.split('T')[0] + ' ' + t.split('T')[1].split(':')[0] for t in df['time']]
    lats = df['latitude']
    lons = df['longitude']
    return dates, lats, lons
    
cabs_df, earthquakes_df = read_and_transform_data()
visualize(cabs_df)

