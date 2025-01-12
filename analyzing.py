# import the csv file
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import folium

# Read the csv file
df = pd.read_csv('./data/flickr_data2.csv', low_memory=False)

df_no_duplicates = df.drop_duplicates(keep='first', inplace=False)

print(len(df_no_duplicates))

df_no_null = df_no_duplicates.dropna(subset=[' lat', ' long', ' date_taken_minute', ' date_taken_hour', ' date_taken_day', ' date_taken_month', ' date_taken_year', ' date_upload_minute', ' date_upload_hour', ' date_upload_day', ' date_upload_month', ' date_upload_year'], inplace=False)


print(len(df_no_null))



# Convert all date columns to numeric, forcing errors to NaN
date_columns = [' date_taken_minute', ' date_taken_hour', ' date_taken_day', ' date_taken_month', ' date_taken_year', 
                ' date_upload_minute', ' date_upload_hour', ' date_upload_day', ' date_upload_month', ' date_upload_year']

for col in date_columns:
    df_no_null.loc[:, col] = pd.to_numeric(df_no_null[col], errors='coerce')

# Drop rows with NaN values in any of the date columns
df_clean = df_no_null.dropna(subset=date_columns, inplace=False)

print(len(df_clean))

# change the type of a column
for col in date_columns:
    df_clean.loc[:, col] = df_clean[col].astype(int)

# Define the ranges for each column
ranges = {
    ' lat': (-90, 90),
    ' long': (-180, 180),
    ' date_taken_minute': (0, 59),
    ' date_taken_hour': (0, 23),
    ' date_taken_day': (1, 31),
    ' date_taken_month': (1, 12),
    ' date_taken_year': (1900, 2021),
    ' date_upload_minute': (0, 59),
    ' date_upload_hour': (0, 23),
    ' date_upload_day': (1, 31),
    ' date_upload_month': (1, 12),
    ' date_upload_year': (1900, 2021)
}

# Filter the dataframe based on the defined ranges
for col, (min_val, max_val) in ranges.items():
    df_clean = df_clean.loc[(df_clean[col] >= min_val) & (df_clean[col] <= max_val)]

# convert the dataframe to csv
df_clean.to_csv('./data/flickr_data2_cleaned.csv', index=False)

print(len(df_clean))

# Example list of latitude and longitude coordinates
# coordinates = [
#     (48.8566, 2.3522),  # Paris
#     (51.5074, -0.1278),  # London
#     (40.7128, -74.0060),  # New York
#     (35.6895, 139.6917)   # Tokyo
# ]
# Extract latitude and longitude coordinates from the dataframe
coordinates = list(set(zip(df_clean[' lat'], df_clean[' long'])))

print(len(coordinates))

# Create a Folium map centered on the average coordinates
# Define the coordinates for Lyon
lyon_center = [45.75, 4.85]  # Approximate center of Lyon
map = folium.Map(location=lyon_center, zoom_start=13)

# Define the bounds for Lyon, similar to the Leaflet example
lyon_bounds = [[45.696, 4.752], [45.85, 4.9]]

# Fit the map to the bounds
map.fit_bounds(lyon_bounds)

# Add markers to the map for the first 50 coordinates only
for lat, lon in coordinates[:50]:
    folium.Marker(location=(lat, lon), popup=f"Lat: {lat}, Lon: {lon}").add_to(map)

# Save the map to an HTML file
map.save("map.html")



