from rake_nltk import Rake
import json

doi = "10.1145.3351095.3372826"
text = open(f"dataset/{doi}/{doi}.txt").read()

r = Rake(min_length=1, max_length=8, include_repeated_phrases=False)
r.extract_keywords_from_text(text)
ranked_keywords = r.get_ranked_phrases()
top_keywords = ranked_keywords[:5000]

# Get all terms from index_terms.json
#  note. this gets all leaves in the json i.e. lowest level terms
term_tree = json.load(open("index_terms.json"))

terms = []
queue = [term_tree]
keyword_set = []

while(queue):
    curr_dict = queue.pop()
    for key in curr_dict:
        if(curr_dict[key]):
            queue.append(curr_dict[key])
        else:
            terms.append(key)

with open(f"keywords.txt", "w") as file:
    for i, keyword in enumerate(top_keywords, start=1):
        file.write(f"{keyword.capitalize()}\n")
        keyword_set.append(f"{keyword.capitalize()}")

acm_words = set(terms)
keywords = set(keyword_set)
overlapping_keywords = keywords.intersection(acm_words)
overlapping_keywords = sorted(list(overlapping_keywords))

if overlapping_keywords:
    print("Overlapping keywords with 'index_terms.json':")
    for keyword in overlapping_keywords:
        print(f"- {keyword}")
else:
    print("No overlapping keywords with 'index_terms.json'.")
