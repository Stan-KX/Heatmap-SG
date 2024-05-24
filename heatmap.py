import os
import pandas as pd
import requests
import folium
from folium.plugins import HeatMap

# Get the directory of the script or executable
dir_path = os.path.dirname(os.path.realpath(__file__))

# Load the dataset
df = pd.read_csv(os.path.join(dir_path, "heatmap.csv"))

# Initialize an empty list to store the latitude and longitude pairs
lat_long_list = []

# Iterate over the addresses in the dataframe
for address in df['Address']:
    # Format the URL with the address
    url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={address}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
    
    # Send a GET request to the API
    response = requests.get(url)
    
    # Convert the response text to a dictionary
    results_dict = response.json()
    
    # Check if there are any results
    if len(results_dict["results"]) > 0:
        # Extract the latitude and longitude from the first result
        latitude = float(results_dict["results"][0]["LATITUDE"])
        longitude = float(results_dict["results"][0]["LONGITUDE"])
        
        # Append the latitude and longitude as a tuple to the list
        lat_long_list.append((latitude, longitude))

# Create a map centered around Singapore
map_object = folium.Map(location=[1.290270, 103.851959], zoom_start=12)

# Add a heatmap to the map using the list of latitude and longitude pairs
HeatMap(lat_long_list).add_to(map_object)

# Save the map to an HTML file
map_object.save(os.path.join(dir_path, 'heatmap.html'))

# Print a success message
print("Heatmap has been created and saved as heatmap.html")
