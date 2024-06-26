import folium
from folium.plugins import HeatMap, MarkerCluster

# Import modules
from modules.extract_coordinates import extract_coordinates

# Create empty lists to store placenames, latitudes, and longitudes
placenames = []
latitudes = []
longitudes = []

# Open the GEDCOM file
with open('family_tree.ged', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Initialize some variables
current_place = None
latitude = None
longitude = None
    
# Loop over each line in the file
for i, line in enumerate(lines):

    # Remove any leading or trailing whitespace from the line
    line = line.strip()
        
    # Check if the line starts with the `2 PLAC` tag
    if line.startswith('2 PLAC'):
                
        # Update the current place
        current_place = line[7:]
        
        # Get the next line and remove any leading or trailing whitespace
        next_line = lines[i+1].strip() if i+1 < len(lines) else None
                        
        # If the next line contains the `3 MAP` tag
        if next_line and '3 MAP' in next_line:

            # Extract the coordinates
            extract_coordinates(lines, i+2, current_place, placenames, latitudes, longitudes)

        # If the next line does not contain the `3 MAP` tag
        else:
            # Get the jurisdiction of the place
            diff_jurisdiction = current_place.partition(',')[2].strip()

            # If the jurisdiction is not empty
            if diff_jurisdiction:

                # Iterate over the lines in the file again
                for j, line in enumerate(lines):

                    # If the line contains the jurisdiction
                    if '2 PLAC ' + diff_jurisdiction in line:

                        # Get the next line and remove any leading or trailing whitespace
                        next_line = lines[j+1].strip() if j+1 < len(lines) else None
                                        
                        # If the next line contains the `3 MAP` tag
                        if next_line and '3 MAP' in next_line:

                            # Extract the coordinates
                            extract_coordinates(lines, j+2, current_place, placenames, latitudes, longitudes)

                            break

    # Reset the variables so we can start looking for the next place
    current_place = None
    latitude = None
    longitude = None

# Check if we found any locations in the GEDCOM file
if len(placenames) == 0:
    print('No locations found in GEDCOM file.')
else:
    # Create a map centered on the first location
    m = folium.Map(location=[float(latitudes[0]), float(longitudes[0])], zoom_start=7)

    # Create a list of coordinate pairs
    coordinates = list(zip(latitudes, longitudes))

    # Create a heatmap layer from the coordinates
    heat_layer = HeatMap(coordinates, name='Heatmap')

    # Add the heatmap layer to the map
    heat_layer.add_to(m)

    # Create a marker cluster
    marker_cluster = MarkerCluster(name='Markers', show=False).add_to(m)

    # Create a dictionary to store unique names and their coordinates
    unique_markers = {}

    # Add markers for each unique location to the map
    for name, lat, lon in zip(placenames, latitudes, longitudes):
        if name not in unique_markers:
            unique_markers[name] = [float(lat), float(lon)]

    # Add the unique markers to the marker cluster
    for name, coords in unique_markers.items():
        folium.Marker(coords, popup=name).add_to(marker_cluster)

    # Add a layer control to the map to toggle the markers
    folium.LayerControl(collapsed=False).add_to(m)

    # Display the map
    m.save('build/map.html')
