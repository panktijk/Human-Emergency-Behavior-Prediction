import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def epoch_to_datetime(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))

col_names = ['Cab_ID', 'Latitude', 'Longitude', 'Whether_Occupied', 'Timestamp']
df = pd.read_csv('Datasets\\cabsdata.csv', names = col_names)
df['Timestamp'] = df['Timestamp'].apply(lambda epoch: epoch_to_datetime(epoch))
df = df[df['Cab_ID'] <= 2]

m = Basemap(width=20000,height=20000,projection='lcc', resolution='f',lat_0=37.76,lon_0=-122.4)
m.drawcoastlines(linewidth=0.5)
m.drawcountries(linewidth=0.5)
#m.fillcontinents(color = 'gray')
colors = {1:'blue', 2:'green'}
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='white',lake_color='aqua')
df = df[df['Whether_Occupied'] == 1]
for row in df.groupby('Cab_ID').head(50):
    lat = df['Latitude'].values
    lon = df['Longitude'].values
    x,y = m(lon, lat)
    m.plot(x, y, 'ro', markersize=5)
    plt.plot(x, y, '-', color=df['Cab_ID']) 
plt.show()