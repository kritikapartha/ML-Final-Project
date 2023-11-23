from bs4 import BeautifulSoup
import requests

# Replace 'url' with the actual URL of the ACM Digital Library page
url = 'https://dl-acm-org.ezproxy.lib.vt.edu/doi/10.1145/3508072.3508106#sec-terms'

# Send a request to the URL and get the HTML content
response = requests.get(url)
html_content = response.text

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the element containing index terms
index_terms_element = soup.find('div', class_='rlist organizational-chart')

# Extract the text content of the index terms
if index_terms_element:
    index_terms = index_terms_element.get_text()
    print(index_terms)
else:
    print("Index terms not found.")
