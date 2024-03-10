import csv
import requests
from bs4 import BeautifulSoup
import validators
from urllib.parse import urlparse
import time
from collections import OrderedDict

# Function to get phone numbers, addresses, and localities from a webpage
def get_contact_info(url, headers):
    contact_info = []

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        h2_elements = soup.find_all('h2', class_='n')  # For 'h2' elements
        div_elements = soup.find_all('div', class_='info')  # For 'div' elements

        for address_element in h2_elements:
            name_element = address_element.find('a', class_='business-name')
            name = name_element.get_text(strip=True) if name_element else ''
            contact_info.append({"name": name, "other_details": []})

        for i, address_element in enumerate(div_elements):
            phone_number_element = address_element.find('div', class_='phones phone primary')
            street_address_element = address_element.find('div', class_='street-address')
            locality_element = address_element.find('div', class_='locality')

            phone_number = phone_number_element.get_text(strip=True) if phone_number_element else ''
            street_address = street_address_element.get_text(strip=True) if street_address_element else ''
            locality = locality_element.get_text(strip=True) if locality_element else ''

            contact_info[i]["other_details"].append(
                {"street_address": street_address, "locality": locality, "phone_number": phone_number}
            )

    except Exception as e:
        print(f"Error in get_contact_info: {e}")

    return contact_info

# Function to scrape contact info from the main page of the website
def scrape_main_page(base_url, headers):
    all_contact_info = []

    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Process contact info on the main page
        contact_info = get_contact_info(base_url, headers)
        all_contact_info.extend(contact_info)

    except Exception as e:
        print(f"Error in scrape_main_page: {e}")

    return all_contact_info

# Function to save contact info to a CSV file in the script's location
def save_to_csv(contact_info, base_url):
    try:
        # Get the base website name for naming the CSV file
        base_website_name = urlparse(base_url).netloc.replace('.', '-')

        # Remove duplicates while preserving the order
        seen = set()
        unique_contact_info = [contact for contact in contact_info if not (contact["name"] in seen or seen.add(contact["name"]))]

        # Dynamically generate the CSV filename
        filename = f"{base_website_name}.csv"

        with open(filename, 'w', newline='', encoding='utf-8', errors='replace') as csvfile:
            fieldnames = ["name", "street_address", "locality", "phone_number"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#            writer.writeheader()

            for contact in unique_contact_info:
                for details in contact["other_details"]:
                    writer.writerow({"name": contact["name"], **details})

        print(f"Saved to '{filename}' in the script's location.")
    except Exception as e:
        print(f"Error in save_to_csv: {e}")

if __name__ == "__main__":
    # Prompt user for the website URL
    base_url = input("Enter the website URL: ").strip()

    # Check if the user provided a valid URL
    if not validators.url(base_url):
        print("Invalid URL. Please provide a valid URL.")
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        contact_info = scrape_main_page(base_url, headers)

        if contact_info:
            save_to_csv(contact_info, base_url)
        else:
            print("No contact info found on the main page of the provided website.")