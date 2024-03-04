import csv
import os
from geopy.geocoders import Nominatim

def geocode_address(address):
    geolocator = Nominatim(user_agent="geocoder_app")
    try:
        location = geolocator.geocode(address, timeout=10)  # Adjust timeout as needed
        if location:
            return location.latitude, location.longitude
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        print(f"Geocoding error: {e}")
    return None, None

def replace_quotes(entry):
    # Replace triple double-quotes with double quotes
    return entry.replace('"""', '"')

# Ask user for input CSV file
input_csv = input("Enter the path to the CSV file with addresses: ")

# Ask user for the business name
business_name = input("Enter the business name: ")

# Ask user for the name of the new CSV file
output_csv = input("Enter the name of the new CSV file (without extension): ") + ".csv"

# Read addresses from input CSV and geocode them
with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        address = row[0]  # Assuming the address is in the first column
        latitude, longitude = geocode_address(address)
        row = [longitude, latitude, f'"{business_name}"'] + row
        writer.writerow(row)

# Now replace triple double-quotes with a single double-quote in the entire CSV file
with open(output_csv, 'r') as file:
    data = file.read()

data = replace_quotes(data)

with open(output_csv, 'w') as file:
    file.write(data)

print(f"Geocoding completed. Results saved to {output_csv}")
