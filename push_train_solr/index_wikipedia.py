#!/usr/bin/env python
from os import error
import sys
import gzip
import json
import pysolr


COMMIT_FREQ = 1000 
solr = pysolr.Solr('http://localhost:8983/solr/test', timeout=10)
count = 0
solr.delete(q='*:*')
solr.commit()
print("Index cleaned")
print("Indexing")
documents = []
# with gzip.open(sys.argv[1],'r') as fin:
#     print(fin)

file = open(sys.argv[1],)
# returns JSON object as 
# a dictionary
data = json.load(file)
for document in data:
    def remove(field):
        if field in document: del document[field]

    # document['title'] = document['Lit_title']
    # del document['Lit_title']
    
    # print(document['Citation_count'])
    # document['citations'] = document['Citation_count']
    # del document['Citation_count']
    
    # for field in ['publication_type','publisher','abstract_structured','snip','sjr','KW_hit_in_kw','cst','csc','KW_hit_in_abstract','KW_hit_in_all','authors_all_count']: 
    #     remove(field)
    for field in ['Language','publisher',"Access_Type","EID","doi","url","Issue","Volume","ENTRYTYPE"]:
        remove(field)
    
    document['title'] = document['Title']
    del document['Title']

    try:
        documents.append(document) 
    except Exception as e:
        print(e)
        print("Article: ",json.dumps(document))
        continue
    
    count+=1
    print('processed {0} articles\r'.format(count)) 
    sys.stdout.flush()
    #if count % COMMIT_FREQ == 0: 
    solr.add(document)
    solr.commit() 
    documents = []

# solr.add(documents)
# solr.commit()