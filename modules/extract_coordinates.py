def extract_coordinates(lines, index, place, placenames, latitudes, longitudes):
    # Get the next two lines, which should contain the latitude and longitude
    lat_line = lines[index].strip()
    long_line = lines[index + 1].strip() if index + 1 < len(lines) else None

    # Check if the longitude line exists
    if long_line is not None:
        # Extract the latitude and longitude
        latitude = lat_line.split(' ')[-1][1:]  # Remove the 'N' from the start of the latitude
        longitude = long_line.split(' ')[-1][1:]  # Remove the 'E' from the start of the longitude
                
        # Add the place name, latitude, and longitude to the lists
        placenames.append(place)
        latitudes.append(latitude)
        longitudes.append(longitude)