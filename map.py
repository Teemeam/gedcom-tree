import folium
from folium.plugins import HeatMap

# Create empty lists to store placenames, latitudes, and longitudes
placenames = []
latitudes = []
longitudes = []

# Open the GEDCOM file
with open("family_tree.ged", "r", encoding="utf-8") as f:

    # Initialize some variables
    current_place = None
    latitude = None
    longitude = None
    
    # Loop over each line in the file
    for line in f:

        # Strip any leading or trailing whitespace from the line
        line = line.strip()
        
        # Check if the line starts with "2 PLAC"
        if line.startswith("2 PLAC"):
                
            # Update the current place
            current_place = line[7:]
            latitude = None
            longitude = None
        
        # Check if the line starts with "4 LATI"
        elif line.startswith("4 LATI"):
            latitude = line.split(" ")[-1][1:]
            
        # Check if the line starts with "4 LONG"
        elif line.startswith("4 LONG"):
            longitude = line.split(" ")[-1][1:]
    
        # If we have a current place, latitude, and longitude, add them to the lists
        if current_place and latitude and longitude:
            placenames.append(current_place)
            latitudes.append(latitude)
            longitudes.append(longitude)

            # Reset the variables so we can start looking for the next place
            current_place = None
            latitude = None
            longitude = None

# Check if we found any locations in the GEDCOM file
if len(placenames) == 0:
    print("No locations found in GEDCOM file.")
else:
    # Create a map centered on the first location
    m = folium.Map(location=[float(latitudes[0]), float(longitudes[0])], zoom_start=7)

    # Create a list of coordinate pairs
    coordinates = list(zip(latitudes, longitudes))

    # Add markers for each location to the map
    for name, lat, lon in zip(placenames, latitudes, longitudes):
        folium.Marker([float(lat), float(lon)], popup=name).add_to(m)

    # Create a heatmap layer from the coordinates
    heat_layer = HeatMap(coordinates)

    # Add the heatmap layer to the map
    heat_layer.add_to(m)

    # Display the map
    m.save("build/map.html")
