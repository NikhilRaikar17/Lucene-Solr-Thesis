import urllib.request
import simplejson
import chardet
import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import json
from wordcloud import WordCloud
import nltk
from nltk import pos_tag
from nltk.stem import PorterStemmer
from nltk import word_tokenize

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

#Extract author titles and place it in corpus list
def extract_titles():
    corpus=[]
    corpus_1 = []
    #file_name = 'scopus.csv'
    file_name = 'results.csv'
    #file_name = 'PLEASE ENTER THE DIR OF THE DATABASE'
    df = pd.read_csv(file_name,encoding='mac_roman')
    data=df.iloc[:,2:3] 
    for index,row in data.iterrows():
        #stemmed_title = lambda x: stem(row['Title']) As of now not used!
        corpus.append(row['Title'])
    return corpus

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
    corpus = extract_titles()
    vectorizer = TfidfVectorizer(stop_words={'english'})
    X = vectorizer.fit_transform(corpus)
    # print(vectorizer.get_feature_names())
    # print(X.shape)
    # print(X[0,])
    K = range(2,10)
    for k in K:
        km = KMeans(n_clusters=k, max_iter=200, n_init=10)
        km = km.fit(X)
        Sum_of_squared_distances.append(km.inertia_)
    plot_graphs(K,Sum_of_squared_distances)
    perform_clustering(corpus,X)
    
# Performs elbow method and plots graphs
def plot_graphs(K,Sum_of_squared_distances):
    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()

# Performs actual clustering
def perform_clustering(corpus,X):
    true_k = input("Please enter an optimal cluster value:\n")
    model = KMeans(n_clusters=int(true_k), init='k-means++', max_iter=200, n_init=10)
    model.fit(X)
    labels=model.labels_
    cluster_data=pd.DataFrame(list(zip(corpus,labels)),columns=['Title','cluster'])
    # print(cluster_data.sort_values(by=['cluster']))
    # plot_results(cluster_data,corpus,labels,int(true_k))
    validate_results(cluster_data)

# Plots results of clustering, uses wordcloud module to better visualise the result
def plot_results(cluster_data,corpus,labels,true_k):
    result={'cluster':labels,'Article_Titles':corpus}
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

def validate_results(cluster_data):
    primary_data = []
    true_value = []
    predicted_value = []
    file_name = 'results.csv'
    df = pd.read_csv(file_name,encoding='mac_roman')
    data=df.iloc[:,0:3]
    for index,row in data.iterrows():
        for index,row_ in cluster_data.iterrows():
            if row_["Title"] == row["Title"] and row["primary"] == 1:
                true_value.append(int(row["primary"]))
                predicted_value.append(row_["cluster"])
                print(row_["Title"],row_["cluster"])
    
    print(true_value)
    print(predicted_value)
    print(metrics.rand_score(true_value, predicted_value))
            


if __name__ == "__main__":
    clustering()

