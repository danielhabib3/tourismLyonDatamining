# import the csv file
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import folium
from sklearn.cluster import KMeans
import os
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.cluster import AgglomerativeClustering

def clean_data(file):
    date_columns = ['date_taken_minute', 'date_taken_hour', 'date_taken_day', 'date_taken_month', 'date_taken_year', 
                    'date_upload_minute', 'date_upload_hour', 'date_upload_day', 'date_upload_month', 'date_upload_year']
    
    all_columns = date_columns + ['lat', 'long']

    # Read the csv file
    df = pd.read_csv(file, low_memory=False) # 420240 rows

    # Strip leading spaces from column names
    df.columns = df.columns.str.strip()

    # Drop duplicates
    df_no_duplicates = df.drop_duplicates(keep='first', inplace=False) # 168107 rows

    # Drop rows with missing values in any of the columns
    df_no_null = df_no_duplicates.dropna(subset=all_columns, inplace=False) # 168107 rows

    # Convert all date columns to numeric, forcing errors to NaN
    for col in date_columns:
        df_no_null.loc[:, col] = pd.to_numeric(df_no_null[col], errors='coerce')

    # Drop rows with NaN values in any of the date columns
    df_clean = df_no_null.dropna(subset=date_columns, inplace=False) # 168057 rows

    df_clean = df_clean.copy()
    # change the type of every date column to int
    for col in date_columns:
        df_clean[col] = df_clean[col].astype(int)


    # Define the ranges for each column
    ranges = {
        'lat': (-90, 90),
        'long': (-180, 180),
        'date_taken_minute': (0, 59),
        'date_taken_hour': (0, 23),
        'date_taken_day': (1, 31),
        'date_taken_month': (1, 12),
        'date_taken_year': (1900, 2021),
        'date_upload_minute': (0, 59),
        'date_upload_hour': (0, 23),
        'date_upload_day': (1, 31),
        'date_upload_month': (1, 12),
        'date_upload_year': (1900, 2021)
    }

    # Filter the dataframe based on the defined ranges
    for col, (min_val, max_val) in ranges.items():
        df_clean = df_clean.loc[(df_clean[col] >= min_val) & (df_clean[col] <= max_val)]

    # convert the dataframe to csv
    df_clean.to_csv('./data/flickr_data2_cleaned.csv', index=False) 
    # 168056 rows if the point is valid
    # 157842 rows if the point is valid and in lyon
    print('Data cleaned and saved to ./data/flickr_data2_cleaned.csv')
    return df_clean

def generate_map(coordinates, k, name='./maps/map.html'):
    # coordinates must be a list of tuples
    # coordinates = list(set(zip(df['lat'], df['long'])))
    # dm.generate_map(coordinates, 1000)  # Générer la carte

    if k == -1:
        k = len(coordinates)

    # colors
    colors = ['lightgray', 'green', 'darkred', 'black', 'darkgreen', 'white', 'orange', 'pink', 'blue', 'gray', 'lightgreen', 'beige', 'darkblue', 'lightblue', 'darkpurple', 'cadetblue', 'lightred', 'red', 'purple']

    # Define the coordinates for Lyon
    lyon_center = [45.75, 4.85]  # Approximate center of Lyon
    map = folium.Map(location=lyon_center, zoom_start=13)

    # Define the bounds for Lyon, similar to the Leaflet example
    lyon_bounds = [[45.696, 4.752], [45.85, 4.9]]

    # Fit the map to the bounds
    map.fit_bounds(lyon_bounds)

    # Add markers to the map for the first 50 coordinates only
    for lat, lon, col in coordinates[:k]:
        if col != -1:
            folium.Marker(location=(lat, lon), popup=f"{col}", icon=folium.Icon(color=colors[col%len(colors)])).add_to(map)

    # Save the map to an HTML file
    map.save(name)

def kmeans_algorithm(df, k):
    # utiliser les premiers 1000 lignes
    df_cluster = df[['lat', 'long']]
    # create a model
    kmeans = KMeans(n_clusters=k, init='k-means++')
    # fit scaled data
    kmeans.fit(df_cluster)

    # add the cluster labels to the dataframe
    df['cluster_kmeans'] = kmeans.labels_
    return df

def elbow(df_cluster):
    # create a list to store the sum of squared distances
    inertia_values = []
    # create a range of k values
    k_values = range(1, 25)
    # loop over k values
    for k in k_values:
        # create a model
        kmeans = KMeans(n_clusters=k, init='k-means++')
        # fit the model
        kmeans.fit(df_cluster)
        # store the sum of squared distances
        inertia_values.append(kmeans.inertia_)

    # plot the elbow method
    plt.figure(figsize=(8, 6))
    plt.plot(k_values, inertia_values, marker='o')
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Sum of squared distances')

    # Annotate each point with its x value
    for i, txt in enumerate(k_values):
        plt.annotate(txt, (k_values[i], inertia_values[i]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.savefig('elbow.png')  # Enregistrer l'image
    # On peut voir que la valeur de k est 5

def agglomerative_clustering(df_cluster, df):
    # Agglomerative Clustering
    # create a list of linkage options
    linkage_options = ['complete', 'average', 'single']

    # create a model
    model = AgglomerativeClustering(n_clusters=100, linkage=linkage_options[2])
    # fit the model
    model.fit(df_cluster)
    # add the cluster labels to the dataframe
    df['agglomerative_cluster'] = model.labels_

    # number of clusters
    n_clusters = len(set(df['agglomerative_cluster'])) - (1 if -1 in df['agglomerative_cluster'] else 0)
    print(f"Number of clusters: {n_clusters}")
    # number of noise points
    n_noise = list(df['agglomerative_cluster']).count(-1)
    print(f"Number of noise points: {n_noise}")

    coordinates = list(set(zip(df['lat'], df['long'], df['agglomerative_cluster'])))
    generate_map(coordinates, 1000, "./maps/mapVieuxLyon.html")  # Générer la carte
    # dm.generate_map(coordinates, 1000)  # Générer la carte

    return df
