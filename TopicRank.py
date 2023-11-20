"""
Code set up:
https://derwen.ai/docs/ptr/start/

Code examples pulled from:
https://derwen.ai/docs/ptr/sample/
"""
import spacy
import pytextrank
import graphviz as gv

# example text
text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types."

# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank to the spaCy pipeline
nlp.add_pipe("textrank")
# nlp.add_pipe("topicrank")
doc = nlp(text)

tr = doc._.textrank

# Print summary of article
for line in tr.summary():
    print(line)
    

# Print out nodes and edges of word graph
print(tr.node_list)
print(tr.edge_list)

# Export word graph
tr.write_dot(path="lemma_graph.dot")

# View exported graph
s= gv.Source.from_file("lemma_graph.dot")
s.view()

# examine the top-ranked phrases in the document
# for phrase in doc._.phrases:
#     print(phrase.text)
#     print(phrase.rank, phrase.count)
#     print(phrase.chunks)