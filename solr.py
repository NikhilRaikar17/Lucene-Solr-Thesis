import urllib.request
import simplejson
import chardet
import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import json
#from wordcloud import WordCloud
import nltk
from nltk import pos_tag
from nltk.stem import PorterStemmer
from nltk import word_tokenize
from pybtex.database.input import bibtex
import pybtex.errors
import sys
pybtex.errors.set_strict_mode(False)


FILE_NAME = 'results_4.csv'
BIB_FILE = 'scopus_4.bib'

cluster_on = input("Cluster based on : \n 1. title \n 2. abstract \n 3. both \n  Enter a value: ")
to_cluster_input = int(cluster_on)
if to_cluster_input == 1:
    print("Clustering based on Titles..")
elif to_cluster_input == 2:
    print("Clustering based on Abstract..")
elif to_cluster_input == 3:
    print("Clustering based on Titles and Abstract..")
else:
    print("Invalid input, please enter a number between 1-3")
    sys.exit()


# Extract data from solr which is running locally with the data
def create_df():
    conn = urllib.request.urlopen('http://localhost:8983/solr/datastore/select?q=*%3A*&wt=json')
    rsp = simplejson.load(conn)
    articles = []
    for lis in rsp:
        for each_row in rsp["response"]["docs"]:
            for key,value in each_row.items():
                    if key == "Title":
                        articles.append(value)
    return None

#Extract author titles and place it in title list
def extract_titles():
    title=[]
    abstract = []
    #file_name = 'scopus.csv'
    file_name = FILE_NAME
    bib_file = BIB_FILE
    #file_name = 'PLEASE ENTER THE DIR OF THE DATABASE'
    parser = bibtex.Parser()
    bib_data = parser.parse_file(bib_file)
    df = pd.read_csv(file_name,encoding='mac_roman')
    data=df.iloc[:,2:3]

    if to_cluster_input == 3:
        for index,row in data.iterrows():
            #stemmed_title = lambda x: stem(row['Title']) As of now not used!
            title.append(row['Lit_title'])
            for entry in bib_data.entries.values():
                if row['Lit_title'] == entry.fields['Title']:
                    if 'Abstract' in list(entry.fields.keys()):
                        abstract.append(entry.fields['Abstract'])

            if len(title) == 0 or len(abstract) == 0:
                print("Clustering is not possible since the bib and the result csv dont match")
                sys.exit()
        
        return title,abstract

    elif to_cluster_input == 2:
        for entry in bib_data.entries.values():
            if 'Abstract' in list(entry.fields.keys()):
                abstract.append(entry.fields['Abstract'])
        
        if len(abstract)==0:
            print("Empty abstracts")
            sys.exit()
        return abstract
    
    else:
        for index,row in data.iterrows():
            #stemmed_title = lambda x: stem(row['Title']) As of now not used!
            title.append(row['Lit_title'])
        if len(title)==0:
            print("Empty titles")
            sys.exit()
        return title

# Not used stemming function
def stem(x):
    dirty = word_tokenize(x)
    tokens = []
    for word in dirty:
        if word.strip(".") == "": #this deals with the bug
           pass
        elif re.search(r"\d{1,}", word): #getting rid of digits
           pass
        else:
           tokens.append(word.strip("."))
    tokens = pos_tag(tokens) #
    progress += 1
    stems = " ".join(stemmer.stem(key.lower()) for key, value in  tokens if value != "NNP") #getting rid of proper nouns
    return stems

# Clustering module which takes elbow Method
# To take the optimal number of clusters and
# Cluster them
def clustering():
    Sum_of_squared_distances = []
    vectorizer = TfidfVectorizer(stop_words={'english'})
    if to_cluster_input == 3:
        title,abstract = extract_titles()
        X = vectorizer.fit_transform(title)
        Y = vectorizer.fit_transform(abstract)
        both_columns = True
    elif to_cluster_input == 2:
        abstract = extract_titles()
        Y = vectorizer.fit_transform(abstract)
        title = abstract
        normalised_column_data = Y
        both_columns = False
    else:
        title = extract_titles()
        X = vectorizer.fit_transform(title)
        normalised_column_data = X
        both_columns = False
    
    # print(vectorizer.get_feature_names())
    # print(X.shape)
    # print(X[0,])
    K = range(2,10)
    
    if both_columns:
        for k in K:
            km = KMeans(n_clusters=k, max_iter=200, n_init=10)
            km = km.fit(X,Y)
            Sum_of_squared_distances.append(km.inertia_)
        plot_graphs(K,Sum_of_squared_distances)
        perform_clustering(title,X=X,Y=Y)
    else:
        for k in K:
            km = KMeans(n_clusters=k, max_iter=200, n_init=10)
            km = km.fit(normalised_column_data)
            Sum_of_squared_distances.append(km.inertia_)

        plot_graphs(K,Sum_of_squared_distances)
        perform_clustering(title,X=normalised_column_data)
    
# Performs elbow method and plots graphs
def plot_graphs(K,Sum_of_squared_distances):
    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()

# Performs actual clustering
def perform_clustering(title,X=False,Y=False,both_columns=False):
    true_k = input("Please enter an optimal cluster value:\n")
    model = KMeans(n_clusters=int(true_k), init='k-means++', max_iter=200, n_init=10)
    if both_columns:
        model.fit(X,Y)
    else:
        model.fit(X)

    labels=model.labels_
    cluster_data=pd.DataFrame(list(zip(title,labels)),columns=['Title','cluster'])
    #print(cluster_data.sort_values(by=['cluster']))
    # plot_results(cluster_data,title,labels,int(true_k))
    validate_results(cluster_data)

# Plots results of clustering, uses wordcloud module to better visualise the result
def plot_results(cluster_data,title,labels,true_k):
    result={'cluster':labels,'Article_Titles':title}
    result=pd.DataFrame(result)
    for k in range(0,true_k):
        s=result[result.cluster==k]
        text=s['Article_Titles'].str.cat(sep=' ')
        text=text.lower()
        text=' '.join([word for word in text.split()])
        wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
        print("")
        print("")
        print('Cluster: {}'.format(k))
        print('Titles')

        titles=cluster_data[cluster_data.cluster==k]['Title']
        print(titles.to_string(index=False))
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

# Validate the results!
def validate_results(cluster_data):
    #files = ['results_1.csv','results_2.csv','results_3.csv','results_4.csv','results_5.csv','results_7.csv','results_8.csv','results_9.csv','results_10.csv']
    file_name=FILE_NAME
    #for file_name in files:
    true_value = []
    predicted_value = []
    df = pd.read_csv(file_name,encoding='mac_roman')
    data=df.iloc[:,0:3]

    if to_cluster_input!=2:
        for index,row in data.iterrows():
            for index,row_ in cluster_data.iterrows():
                if row_["Title"] == row["Lit_title"] and row["primary"] == 1:
                    true_value.append(int(row["primary"]))
                    predicted_value.append(row_["cluster"])
                    # print(row_["Title"],row_["cluster"])
    else:
        bib_file = BIB_FILE
        parser = bibtex.Parser()
        bib_data = parser.parse_file(bib_file)
        for index,row in data.iterrows():
            if row["primary"] == 1:
                true_value.append(int(row["primary"]))
                actual_title = row['Lit_title']
                for entry in bib_data.entries.values():
                    if actual_title == entry.fields['Title']:
                        for index,row_ in cluster_data.iterrows():
                            if 'Abstract' in list(entry.fields.keys()) and row_["Title"]==entry.fields['Abstract']:
                                predicted_value.append(row_["cluster"])
                                
    if len(true_value) > 0 or len(predicted_value)>0: 
        print("Primary:", true_value)
        print("Cluster_predicted", predicted_value)
        print("Rand Score:",metrics.rand_score(true_value, predicted_value))
        print("Mallows Score:",metrics.fowlkes_mallows_score(true_value, predicted_value))
        print("")
    else:
        print("Different files, please make sure atleast some titles are there in the file!")


if __name__ == "__main__":
    clustering()
