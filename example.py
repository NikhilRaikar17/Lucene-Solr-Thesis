import urllib3
import urllib
import requests
import json

class Example():
    apiKey = "8ae25cee98ba830956d895f6d2f46255"
    apiKey2 = "25a76f4e439ef1cb5dd7173dfb56fcac"
    apikey3 ="6580d02a3c6cece63fd07a71153aa96e"
    newapikey ="7b234f853f17933508c848a50784125b"
    url = "https://api.elsevier.com/content/search/sciencedirect?"
    url2 = "http://api.elsevier.com/content/serial/title?"
    url3 = "https://api.elsevier.com/analytics/plumx/doi/"
    url_citation = "https://api.elsevier.com/content/abstract/citation-count?"
    url_citation2="http://api.elsevier.com/content/search/scopus?query=DOI("
    url_doi ="https://api.elsevier.com/content/search/scopus?query=title("
    url_doi_all ="https://api.elsevier.com/content/search/scopus?query=doi("
    getVars = {'apiKey': apiKey}
    getVars2 = {'apiKey': apiKey2}
    getVars3 = {'apiKey': apikey3}

    def getPlumxdata(self,doi_lit):
        if doi_lit is "":
            return
        if doi_lit is None:
            return
        else:
            requestUrl = self.url3 + doi_lit + "?" + urllib.parse.urlencode(self.getVars2)
            print(requestUrl)
            req = requests.get(requestUrl)
        try:
            r = req.json()
            # print("i am here")
        except HTTPError as e:
            print('The server couldnt fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            
if __name__ == "__main__":
    example = Example()
    example.getPlumxdata("10.1145/1401890.1401965")