# Imports
from bs4 import BeautifulSoup
import requests
import json
import csv
import re
from PyPDF2 import PdfReader 
import io
import os
import time

# Get all terms from index_terms.json
#  note. this gets all leaves in the json i.e. lowest level terms
term_tree = json.load(open("index_terms.json"))

terms = []
queue = [term_tree]

while(queue):
    curr_dict = queue.pop()
    for key in curr_dict:
        if(curr_dict[key]):
            queue.append(curr_dict[key])
        else:
            terms.append(key)
            
# ACM does not provide more than 2k results per search
#  each search query will return max(2k, PAGE_SIZE*NUM_PAGES) articles
PAGE_SIZE = 50
NUM_PAGES = 1

FIELDS = ['doi', 'pdf'] #Options: 'title', 'url', 'abstract', 'pdf', 'doi'

"""
    Run a search query on ACM
    
    Returns the info in FIELDS about each article returned by search query
"""
def search_acm(search_term):
    results = []
    for page_num in range(NUM_PAGES): 
        url = f'https://dl.acm.org/action/doSearch?AllField={search_term.replace(" ", "+")}&pageSize={PAGE_SIZE}&startPage={page_num}'
        content = requests.get(url).text
        page = BeautifulSoup(content)

        entries = page.find_all("div", attrs={"class": "issue-item__content"})
        if(entries):
            for entry in entries:
                curr_result = {}
                
                for field in FIELDS:
                    if(field == "title"):
                        title = entry.find('h5', attrs={'class': 'issue-item__title'})
                        curr_result['title'] = title.text.replace('[PDF]','')
                        
                    elif(field == "url"):
                        curr_result["url"] = 'https://dl.acm.org'+entry.a['href']
                        
                    elif(field == "abstract"):
                        abst=entry.find('div', attrs={'class': 'issue-item__abstract'})
                        curr_result["abstract"] = abst.text.replace('\n','')
                    
                    elif(field == "pdf"):
                        pdf=entry.find('a', attrs={'data-title': 'PDF'})
                        curr_result['pdf'] = 'https://dl.acm.org'+pdf["href"] if pdf else ""
                    
                    elif(field == "doi"):
                        curr_result["doi"] = entry.a['href'][5:]
                        
                
                results.append(curr_result)
                
        else:
            print(f"No entries found for search: {url}")
            
    return results

""" 
Returns index terms for a given ACM article

Input is the ACM link to the article 
 e.g. https://dl.acm.org/doi/10.1145/3351095.3372826
"""
def get_index_terms(url):
    # Send a request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the element containing index terms
    index_terms_element = soup.find('ol', class_='rlist organizational-chart')
    
    if(index_terms_element is None):
        print(f"No index terms at: {url}")
        return

    # Parse index term tree
    index_term_tree = {}
    for header in index_terms_element.find_all('li', recursive=False):
        h6 = header.find('h6')
        if h6:
            index_term_tree[h6.text] = {}
            queue = [(header, index_term_tree[h6.text])]
            while queue:
                list_item, curr_tree = queue.pop()
                try:
                    for sub_list_item in list_item.ol.find_all('li', recursive=False):
                        term = sub_list_item.div.p.a.text
                        curr_tree[term] = {}
                        queue.append((sub_list_item, curr_tree[term]))
                except:
                    print("something failed")


    return index_term_tree


"""
Returns the text of a PDF as a string

Input is the ACM link to the PDF
 e.g. https://dl.acm.org/doi/pdf/10.1145/3351095.3372826
"""
def get_pdf_text(url):
    response = requests.get(url=url)
    on_fly_mem_obj = io.BytesIO(response.content)
    reader = PdfReader(on_fly_mem_obj)

    article_text = ""
    for page in reader.pages:
        article_text += page.extract_text().strip() 
        
    return article_text


# Search on all possible index terms and write results to DOIs file
DOI_FILE_NAME = "DOIs.csv"

outfile = open(DOI_FILE_NAME, "w", encoding="utf-8", newline='')
writer = csv.DictWriter(outfile, fieldnames = FIELDS) 
writer.writeheader()
outfile.flush()

OUTPUT_DIR = "./dataset/"


if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

all_results = []   

for search_term in terms:
    results = search_acm(search_term)
    
    print(f"Outputing {len(results)} results for term: {search_term}")
    writer.writerows(results) 
    outfile.flush()
    
    all_results += results
    
    for result in results:
        doi,pdf = result['doi'], result['pdf']
        url = "https://dl.acm.org/doi/" + doi
        
        doi = doi.replace('/', '.') # the '/' is not valid for path naming
        
        if not os.path.exists(os.path.join(OUTPUT_DIR, doi)):
            os.makedirs(os.path.join(OUTPUT_DIR, doi))
        else:
            print(f"Directory already exists. Overwriting {os.path.join(OUTPUT_DIR, doi)}")
        
        term_tree = get_index_terms(url) 
        if(term_tree):
            outfile_terms = open(os.path.join(OUTPUT_DIR, doi, f"{doi}.json"), "w")
            json.dump(term_tree, outfile_terms)
            outfile_terms.close()
        if(pdf):
            outfile_text = open(os.path.join(OUTPUT_DIR, doi, f"{doi}.txt"), "w", 
                        encoding="utf-8", errors="ignore")
            outfile_text.write(get_pdf_text(pdf))
            outfile_text.close()
        print("Outputted doi and pdf")
        time.sleep(30)
        
outfile.close()    



## For every article in DOI file, 
##  - create directory OUTPUT_DIR/{doi}/
##  - get index terms and put in OUTPUT_DIR/{doi}/{doi}.json
##  - get text from pdf and put in OUTPUT_DIR/{doi}/{doi}.txt