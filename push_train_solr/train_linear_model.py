#!/usr/bin/env python
import os
import json
import pysolr
from dataset import Dataset
from rankers import Rankers
import time
import numpy as np

if __name__ == "__main__":

    feature_names = [] 
    dataset = Dataset()
    rankers = Rankers()
    model_name = "model"
    output = 'last-training.txt' 
    with open(output,'w') as fout: 
        for qid,query in enumerate(dataset.get_queries()):
            results = rankers.query('default', query, fl=['id','title','score',f'[features efi.query={query}]'])
            for doc in results:
                docid = doc["id"]
                print(query)
                print(docid)
                if dataset.is_relevant(query, docid): rel=1000
                else: rel = -1
                features = doc["[features]"]
                print(rel)
                print(features)
                fvalues = list(map(lambda x : x.split("=")[1], features.split(",")))
                feature_names = list(map(lambda x : x.split("=")[0], features.split(",")))
                fid = range(len(fvalues))
                print(fvalues)
                feature_str = " ".join(fvalues)
                print(feature_str)
                fout.write(" ".join([str(rel),str(qid), " "]) + feature_str + "\n")
                if rel > 0:
                    for i in range(30): fout.write(" ".join([str(rel),str(qid), " "]) + feature_str+"\n")
#-----------------------------------------------------------------
# Load and train the model
    data = np.loadtxt(output)
    y = data[:,0]
    x = data[:,1:]
    
    weights = np.polyfit(y, x, 1)[0].tolist()
    print(weights)
    print("Linear Model\n  ", "\t \n+ ".join(map(lambda w: str(w)+"\t* ", zip(weights, feature_names))))
    
    model = {} 
    model["class"] = "org.apache.solr.ltr.model.LinearModel"
    model["name"] = model_name 
    model["features"] = [] 
    
    for name in feature_names: 
        model["features"].append({"name": name})
    
    model["params"] = {
            "weights" : {
             }
    } 
    for feature_value, feature in zip(weights, feature_names):
        model["params"]["weights"][feature] = feature_value

    print(model)
    
    # import requests
    # import sys
    # url = 'http://localhost:8983/solr/test/schema/model-store'
    # headers = {"content-type": "application/json"}
    # r = requests.put(url, data=json.dumps(model), headers=headers)
    # if r.status_code != 200:
    #     print("Error uploading the model",r)
    #     sys.exit(-1)
    # ltr_ranker = {}
    # rq = "{!ltr model=%s reRankDocs=%d efi.query=$query}" % (model_name, 30) 
    # ltr_ranker["rq"] = rq
    # rankers.add_ranker(model_name, ltr_ranker)
    # ltr_ranker = {}
    # rq = "{!ltr model=%s reRankDocs=%d efi.query=$query}" % (model_name, 30) 
    # ltr_ranker["rq"] = rq
    # rankers.add_ranker(model_name, ltr_ranker)
    # print("Loaded model: ",model_name)