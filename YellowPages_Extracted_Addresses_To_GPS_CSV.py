import csv
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

# Function to replace triple double-quotes with a single double-quote
def replace_quotes(entry):
    return entry.replace('"""', '"')

# Ask user for input CSV file
input_csv = input("Enter the path to the CSV file with addresses: ")

# Ask user for the business name
business_name = input("Enter the business name: ")

# Ask user for the name of the new CSV file
output_csv = input("Enter the name of the new CSV file (without extension): ") + ".csv"

# Read addresses from input CSV, geocode them, and add phone number to each row
with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        address = row[0]+row[1]  # Assuming the address is in the first column
        latitude, longitude = geocode_address(address)
        locality = row[2]
        phone_number = row[3]  # Assuming the phone number is in the fourth column

        # Concatenate address, state, zip code, and phone number into a single string
        full_address = f"{address},{locality},{phone_number}"
#        full_address = f"{address},{locality}"

        row = [longitude, latitude, f'"{business_name}"',f'"{full_address}"']
        writer.writerow(row)

# Replace triple double-quotes with a single double-quote in the entire CSV file
with open(output_csv, 'r') as file:
    data = file.read()

data = replace_quotes(data)

with open(output_csv, 'w') as file:
    file.write(data)

print(f"Geocoding completed. Results saved to {output_csv}")