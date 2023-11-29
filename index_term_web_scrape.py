from bs4 import BeautifulSoup
import requests

# Replace 'url' with the actual URL of the ACM Digital Library page
url = 'https://dl-acm-org.ezproxy.lib.vt.edu/doi/10.1145/3508072.3508228#sec-terms'

# Send a request to the URL and get the HTML content
response = requests.get(url)
html_content = response.text

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the element containing index terms
index_terms_element = soup.find('ol', class_='rlist organizational-chart')

def parse_tree(ol_element):
    tree = {}
    for li in ol_element.find_all('li', recursive=False):
        h6 = li.find('h6')
        if h6:
            links = li.find_all('a')
            link_texts = [link.text for link in links]
            tree[h6.text] = {'Indexes': link_texts}
    return tree

index_term_tree = parse_tree(index_terms_element)

print("Tree Structure with Indexes:")
print(index_term_tree)
