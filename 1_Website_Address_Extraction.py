import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import validators

# Function to get addresses from a webpage
def get_addresses(url):
    addresses = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find address elements based on the provided HTML structure
        street_elements = soup.find_all('span', class_='c-address-street-1')
        city_elements = soup.find_all('span', class_='c-address-city')
        state_elements = soup.find_all('abbr', class_='c-address-state')
        postal_code_elements = soup.find_all('span', class_='c-address-postal-code')

        # Check if all address components are present before adding to the list
        if street_elements and city_elements and state_elements and postal_code_elements:
            for street, city, state, postal_code in zip(street_elements, city_elements, state_elements, postal_code_elements):
                address = f"{street.get_text(strip=True)}, {city.get_text(strip=True)}, {state.get_text(strip=True)}, {postal_code.get_text(strip=True)}"
                addresses.append(address)

    except Exception as e:
        print(f"Error in get_addresses: {e}")

    return addresses

# Function to scrape addresses from linked pages
def scrape_website(base_url):
    all_addresses = []

    try:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Modify this part based on how the links are structured on the website
        links = soup.find_all('a', href=True)  # Change this based on your HTML structure

        for link in links:
            absolute_link = urljoin(base_url, link['href'])
            print(f"Processing link: {absolute_link}")
            addresses = get_addresses(absolute_link)
            print(f"Addresses found: {addresses}")
            all_addresses.extend(addresses)

    except Exception as e:
        print(f"Error in scrape_website: {e}")

    return all_addresses

# Function to save addresses to a CSV file in the script's location
def save_to_csv(addresses, base_url):
    try:
        # Get the base website name for naming the CSV file
        base_website_name = urlparse(base_url).netloc.replace('.', '-')

        # Remove duplicates
        unique_addresses = list(set(addresses))

        # Dynamically generate the CSV filename
        filename = f"{base_website_name}.csv"

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[address] for address in unique_addresses])
        print(f"Addresses saved to '{filename}' in the script's location.")
    except Exception as e:
        print(f"Error in save_to_csv: {e}")

if __name__ == "__main__":
    # Prompt user for the website URL
    base_url = input("Enter the website URL: ").strip()

    # Check if the user provided a valid URL
    if not validators.url(base_url):
        print("Invalid URL. Please provide a valid URL.")
    else:
        addresses = scrape_website(base_url)

        if addresses:
            save_to_csv(addresses, base_url)
        else:
            print("No addresses found on the provided website.")
