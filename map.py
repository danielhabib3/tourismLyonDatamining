import folium

# Example list of latitude and longitude coordinates
coordinates = [
    (48.8566, 2.3522),  # Paris
    (51.5074, -0.1278),  # London
    (40.7128, -74.0060),  # New York
    (35.6895, 139.6917)   # Tokyo
]

# Create a Folium map centered on the average coordinates
map_center = [sum(x)/len(coordinates) for x in zip(*coordinates)]
map = folium.Map(location=map_center, zoom_start=2)

# Add markers to the map
for lat, lon in coordinates:
    folium.Marker(location=(lat, lon), popup=f"Lat: {lat}, Lon: {lon}").add_to(map)

# Save the map to an HTML file
map.save("map.html")

# To display the map in a Jupyter Notebook, use this:
map
