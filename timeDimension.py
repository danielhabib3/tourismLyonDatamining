# import the csv file
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import folium
import os
from sklearn.cluster import KMeans
import datamining as dm  # contains clean_data, generate_map
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import time
from datetime import datetime
from sklearn.preprocessing import StandardScaler



file_path = './data/flickr_data2_cleaned.csv'

# List of files to delete if they exist
files_to_delete = ['./maps/map.html', './elbow_charts/elbow.png', './elbow_charts/distance_to_4th_nearest_point.png', './maps/mapLargestCluster.html']

# Loop through the list and delete each file if it exists
for file in files_to_delete:
    if os.path.exists(file):
        os.remove(file)

# df has to contain 157842 rows
if not(os.path.exists(file_path)):
    print('Data file not found. Cleaning data...')
    df = dm.clean_data('./data/flickr_data2.csv')
else:
    print('Data file found. Reading data...')
    df = pd.read_csv(file_path, low_memory=False)


# Create unix time stamp
df['unix_timestamp'] = df.apply(lambda row: int(pd.Timestamp(year=row['date_taken_year'], month=row['date_taken_month'], day=row['date_taken_day'], hour=row['date_taken_hour'], minute=row['date_taken_minute']).timestamp()), axis=1)

df_cluster = df[['lat', 'long', 'unix_timestamp']]  # Extract the coordinates for clustering

# standardize the unix_timestamp, lat and long using standard scaler
scaler = StandardScaler()
df_cluster[['lat', 'long', 'unix_timestamp']] = scaler.fit_transform(df_cluster[['lat', 'long', 'unix_timestamp']])

# Dbscan algorithm
dbscan = DBSCAN(eps=0.3, min_samples=10)
dbscan.fit(df_cluster)
df['event'] = dbscan.labels_

# number of clusters
n_clusters = len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0)
print('Number of clusters:', n_clusters)

#noise
n_noise = list(dbscan.labels_).count(-1)
print('Number of noise:', n_noise)

coordinates = list(set(zip(df['lat'], df['long'], df['event'])))
dm.generate_map(coordinates, 1000, './maps/eventMap.html')




# # extract date from unix_timestamp
# date = datetime.utcfromtimestamp(df_cluster.iloc[0]['unix_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
# print("Date:", date)






