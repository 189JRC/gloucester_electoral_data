import requests
from bs4 import BeautifulSoup
import time

def crawl_and_save(url, output_file, node=0):
    # Set up a session for making HTTP requests
    session = requests.Session()

    # Fetch the content of the provided URL
    try:
        response = session.get(url)
        response.raise_for_status()  # Check if the request was successful
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return
    
    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract and save the page content to a text file
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(soup.get_text())

    print(f"Content from {url} saved to {output_file}")

    if node == 0:
        # Find all links on the page and crawl them
        links = soup.find_all('a', href=True)

        links_valid = [] 
        link_filter = {
        "elmbridge",
        "longlevens",
        "kingholm",
        "barnwood",
        "abbeymead",
        "hucclecote",
        "westgate",
        "barton",
        "matson",
        "abbeydale",
        "coney",
        "tuffley",
        "westgate",
        "kingsway",
        "quedgeley",
        "grange",
        "podsmead",
        "moreland",
        "churchdown"
        }
        for link in links:
            # for link_f in link_filter:
                try:
                    _ = link['title'].lower()
                    for ward_name in link_filter:
                        if ward_name in link['title'].lower():
                            links_valid.append(link)
                            link_filter.delete(ward_name)
                            print("added", link['href'])
                except:
                    pass
                


        for link in links_valid:
            next_url = "https://democracy.gloucester.gov.uk/" + link['href']
            print(f"Crawling link: {next_url}")
            crawl_and_save(next_url, 'output.txt', node=1)  # Recurse on the next link
            time.sleep(1)  # Be polite and don't overload the server

# Example usage:
url = "https://democracy.gloucester.gov.uk/mgElectionResults.aspx?ID=17&V=1&RPID=56987338"
output_file = "page_content.txt"
crawl_and_save(url, output_file)


wards = [
    "elmbridge",
    "longlevens",
    "kingholm",
    "barnwood",
    "abbeymead",
    "hucclecote",
    "westgate",
    "barton",
    "matson",
    "abbeydale",
    "coney",
    "tuffley",
    "westgate",
    "kingsway",
    "quedgeley",
    "grange",
    "podsmead",
    "moreland",
    "churchdown"
]