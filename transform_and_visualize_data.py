import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

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
    plt.plot(x, y, '-', color='yellow', linewidth = 1.75)
    
def get_continuous_paths(df):
    splits = np.append(np.where(np.diff(df['Whether_Occupied']) != 0)[0], len(df)+1)+1
    prev = 0
    paths_df = []
    for split in splits:
        paths_df += [df[prev:split]]
        prev = split
    return splits, paths_df
    
def visualize(df):
    splits, paths_df = get_continuous_paths(df)
    m = Basemap(llcrnrlon=-122.56,llcrnrlat=37.4,urcrnrlon=-122,urcrnrlat=37.99, epsg=4269)
    for path_df in paths_df[:50]:
        if path_df.iloc[0]['Whether_Occupied'] == 1:
            trace_trajectory(path_df, m)   
    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 2500, verbose= True)
    plt.figure()
    plt.show()
    
def get_earthquake_dates(df):
    dates = [t.split('T')[0] + ' ' + t.split('T')[1].split(':')[0] for t in df['time']]
    return dates
    
cabs_df, earthquakes_df = read_and_transform_data()
earthquake_dates = get_earthquake_dates(earthquakes_df)
normal_day_cabs_df = cabs_df[~cabs_df['Timestamp'].str.contains('|'.join(earthquake_dates))]
visualize(normal_day_cabs_df)
earthquake_day_cabs_df = cabs_df[cabs_df['Timestamp'].str.contains('|'.join(earthquake_dates))]
visualize(earthquake_day_cabs_df)

