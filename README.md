Use these scripts to help you create large sets of POI files easily by scraping a business's website for its locations.
The resulting CSV's can then be converted to required format i.e. GPX.

I reccomend using the Yellowpages scripts since they work 99% of the time and they extract phone numbers as well.
After running
YellowPages_Address_Extraction.py
Look through csv for any missing addresses before using
YellowPages_Extracted_Addresses_To_GPS_CSV.py
The scripts don't handle addresses with 'Suite or Ste' very well. 
I use https://www.mapdevelopers.com/geocode_tool.php after YellowPages_Extracted_Addresses_To_GPS_CSV.py to fill in any
missing coords.

This site can batch geocode: https://www.geoapify.com/tools/geocoding-online

YellowPages_Address_Extraction-Extended.py
Isn't compatable with YellowPages_Extracted_Addresses_To_GPS_CSV.py for geocoding
to GPS coordinates but it does scrape business names and the CSV can be uploaded to the above website.



CSV-Combine.py
Combines a folder of CSV's into one CSV.

CSV-Combine-2.py
Combines a folder of CSV's into one CSV. Different method, may work if previos does not.

CSV-Combine-3-MisMatch.py
Combines a folder of CSV's into one CSV. If some columns don't have data it will add some so it can append columns.


1_Website_Address_Extraction.py
Uses BeautifulSoup to scrape from a HTML webpage where the store locations addresses are one level down.
For example Jamba Juice. I want all the locations in California. I would go to their state list for CA. https://locations.jamba.com/ca
And input that into the script when it asks for the website. It will then grab and follow the city links and locations from
that page and create a CSV with all the store addresses it finds. In this format "11221 York Rd., Cockeysville, MD, 21030"

1b_Website_Address_Extraction-1sec-Delay.py
This one has a 1 second delay between scans to help mitigate getting blocked by a website for too quick attempts.


2_Website_Extracted_Addresses_To_GPS_CSV.py
This script will ask for location of your newly created CSV, which was named as your input URL, in this case locations-jamba-com.csv.
It will then ask for the businesses name so it can add that to each line in the next CSV which will be in a GPS file
convertible format. -76.723355,39.1596579,"Jamba","7000 Arundel Mills Circle, Hanover, MD, 21076"
There will be a need to touch up or re-geocode some addresses by hand.
