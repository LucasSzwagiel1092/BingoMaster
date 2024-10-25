import requests
from bs4 import BeautifulSoup
import re

def get_item_drop_data(item_name):
    # Set up the API URL for the item
    formatted_item_name = item_name.replace(" ", "_")
    api_url = f"https://oldschool.runescape.wiki/api.php?action=parse&format=json&page={formatted_item_name}&prop=text"

    # Make the API request
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        html_content = data['parse']['text']['*']

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Locate the "Item sources" header
        item_sources_header = soup.find(lambda tag: tag.name == "h2" and "Item sources" in tag.get_text())

        # If the "Item sources" header is found, locate the next table
        drop_sources = []
        if item_sources_header:
            drop_table = item_sources_header.find_next_sibling('table', class_='wikitable')

            # Find all rows in the table and extract monster names and drop rates
            if drop_table:
                for row in drop_table.find_all('tr'):
                    columns = row.find_all('td')

                    # Ensure we have enough columns to represent drop entries
                    if len(columns) >= 4:
                        monster_name = columns[0].get_text(strip=True)
                        drop_chance = columns[3].get_text(strip=True)  # Get the 4th column for drop chance

                        # Check if the drop chance is a valid fraction or numerical value
                        if re.match(r"^\d+/\d+$", drop_chance) or re.match(r"^\d+(\.\d+)?%?$", drop_chance):
                            drop_sources.append((monster_name, drop_chance))

        return drop_sources
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")
