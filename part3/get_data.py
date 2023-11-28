import argparse
import requests
from bs4 import BeautifulSoup
import re


def extract_prices_and_area(input_string):
    # Define the regex patterns for different price formats and area in box
    price_m2_pattern = r'\$(\d+(\.\d+)?)\s*per m2'
    price_box_pattern = r'\$(\d+(\.\d+)?)\s*per box'
    price_each_pattern = r'\$(\d+(\.\d+)?)\s*each'
    area_in_box_pattern = r'\((\d+(\.\d+)?)\s*m2\)'

    # Initialize default values
    price_m2, price_box, price_each, area_in_box = None, None, None, None

    # Search for the different price formats and area
    m2_match = re.search(price_m2_pattern, input_string)
    if m2_match:
        price_m2 = float(m2_match.group(1))

    box_match = re.search(price_box_pattern, input_string)
    if box_match:
        price_box = float(box_match.group(1))

    each_match = re.search(price_each_pattern, input_string)
    if each_match:
        price_each = float(each_match.group(1))

    area_match = re.search(area_in_box_pattern, input_string)
    if area_match:
        area_in_box = float(area_match.group(1))

    return price_m2, price_box, price_each, area_in_box


# Function to read URLs from a file and fetch data
def read_urls_from_file(file_path, num_urls):
    # Initialize a list to hold the data
    data_list = []

    try:
        # Open the file for reading
        with open(file_path, 'r') as file:
            # Read the specified number of URLs or all if num_urls is None
            for i, url in enumerate(file):
                if num_urls is not None and i >= num_urls:
                    break

                # Remove leading/trailing whitespace and newline characters
                url = url.strip()

                # Send a GET request
                response = requests.get(url)

                # Check if the request was successful
                if response.status_code == 200:
                    # Parse the HTML content
                    soup = BeautifulSoup(response.text, 'html.parser')

                    title = soup.find('h1').text
                    price = soup.find('ul', class_='shop-product-prices').find('li').getText(strip=True)
                    price_m2, price_box, price_each, area_in_box = extract_prices_and_area(price)

                    print(f"{url} {title} {price_m2}  {price_box}  {area_in_box}  {price_each}")

                else:
                    print(f"Failed to retrieve data from URL {url}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")

    return data_list


if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Read URLs from a file and fetch data.')

    # Add an argument for the file path
    parser.add_argument('file_path', type=str, help='Path to the text file containing URLs')

    # Add an argument for the number of URLs to fetch (optional)
    parser.add_argument('--num_urls', type=int, help='Number of URLs to fetch (default is all)')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function to read URLs from the file and fetch data
    result_data = read_urls_from_file(args.file_path, args.num_urls)
