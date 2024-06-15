def extract_coordinates(file, place, placenames, latitudes, longitudes):
    # Get the next two lines, which should contain the latitude and longitude
    lat_line = next(file).strip()
    long_line = next(file).strip()

    # Extract the latitude and longitude
    latitude = lat_line.split(' ')[-1][1:]  # Remove the 'N' from the start of the latitude
    longitude = long_line.split(' ')[-1][1:]  # Remove the 'E' from the start of the longitude
                
    # Add the place name, latitude, and longitude to the lists
    placenames.append(place)
    latitudes.append(latitude)
    longitudes.append(longitude)
