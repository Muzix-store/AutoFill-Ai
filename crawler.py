import requests
from bs4 import BeautifulSoup

def crawl_guitar_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    guitar_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']

        if 'gitary' in href:
            guitar_links.append(href)

    return guitar_links

def write_links_to_file(links, filename):
    with open(filename, 'w') as file:

        file.write(f"{len(links)}\n")
        for link in links:
            file.write(f"https://piano.by{link}\n")

url = 'https://piano.by/gitary'
guitar_links = crawl_guitar_links(url)
output_file = './Data/guitar_links.txt'
write_links_to_file(guitar_links, output_file)

print(f"Found {len(guitar_links)} links. Links have been written to {output_file}.")