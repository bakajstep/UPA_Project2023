import requests
from bs4 import BeautifulSoup

base_url = 'https://www.tiledepot.co.nz/browse/tiles/wall-tiles/'
# all_urls = []

# Iterate over all pages(1-3)
for page_number in range(1, 4):
    # URL každé stránky
    url = f'{base_url}/{page_number}/?pp=96'

    # Send a GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.find_all('h4', class_='title-price')

        # Iterate over each product
        for product in products:
            # Find <a> tag and get 'href' attribute
            a_tag = product.find('a')
            if a_tag and a_tag.has_attr('href'):
                print(a_tag['href'])
                # all_urls.append(a_tag['href'])
    else:
        print(f"Failed to retrieve page {page_number}")

# # Store URLs to text file
# with open('urls.txt', 'w') as file:
#     for i, url in enumerate(all_urls):
#         file.write(url)
#         # Check if it's not the last URL to avoid adding a newline
#         if i < len(all_urls) - 1:
#             file.write('\n')
