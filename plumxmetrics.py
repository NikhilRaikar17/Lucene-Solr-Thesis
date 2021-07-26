import urllib, urllib3,json,requests,sys
from pybliometrics.scopus import PlumXMetrics
import pybtex.errors
from pybtex.database.input import bibtex
import pandas as pd
pybtex.errors.set_strict_mode(False)

class get_altmetrics():
    apiKey = "8ae25cee98ba830956d895f6d2f46255"
    apiKey2 = "7f59af901d2d86f78a1fd60c1bf9426a"
    apikey3 ="6580d02a3c6cece63fd07a71153aa96e"
    newapikey ="7b234f853f17933508c848a50784125b"
    new_key_1 ="25a76f4e439ef1cb5dd7173dfb56fcac"
    new_key_2 ="a11cf476ddc87c317e723bd0fbac9540"

    plumx_url = "https://api.elsevier.com/analytics/plumx/doi/"
    
    getVars = {'apiKey': apiKey}
    getVars2 = {'apiKey': apiKey2}
    getVars3 = {'apiKey': apikey3}
    getVars4 = {'apiKey': new_key_1}
    getVars5 = {'apiKey': new_key_2}

    def getPlumxdata(self,doi_lit):
        if doi_lit is "":
            return " "
        if doi_lit is None:
            return " "
        else:
            u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"
            request = self.plumx_url+doi_lit+'?apiKey='+self.apikey3
            print(request)
            response = requests.get(request, headers={"USER-AGENT": u_a})
            try:
                data = response.json()
                
                if "service-error" in data:
                    print("Not able to load the data")
                    sys.exit()
                return data
            except Exception as e:
                print(e)
                return " "
    
    def extract_data(self, data):
        doi_dict = {}
        
        for index,row in data.iterrows():
            doi = row['doi']
            if doi is not None or doi!= '':
                doi = str(doi)
                response = altmetrics.getPlumxdata(doi_lit=doi)
                if response!= "":
                    doi_altmetrics = {}
                    if 'count_categories' in response:
                        for index in range(0, len(response['count_categories'])):
                            name = response['count_categories'][index]['name']
                            total = response['count_categories'][index]['total']   
                            doi_altmetrics[name] = total

                            if 'count_types' in response['count_categories'][index]:
                                for each_index in range(0, len(response['count_categories'][index]['count_types'])):
                                    count_type_name = response['count_categories'][index]['count_types'][each_index]['name'] 
                                    count_type_total = response['count_categories'][index]['count_types'][each_index]['total']
                                    print(count_type_name)
                                    print(count_type_total)
                                    doi_altmetrics[count_type_name] = count_type_total
                    doi_dict[doi] = doi_altmetrics
                    
if __name__ == "__main__":
    
    altmetrics = get_altmetrics()
    
    # -----------------------------------------------------------
    # BIB_FILE = 'scopus_4.bib'
    # bib_file = BIB_FILE
    # parser = bibtex.Parser()
    # bib_data = parser.parse_file(bib_file)
    # for entry in bib_data.entries.values():
    #     doi = str(entry.fields['Doi']).replace("https://doi.org/", "")
    #     if doi is not None or doi!= "":
    #         example.getPlumxdata(doi)
    # ----------------------------------------------------------------------

    CSV_FILE = './data/Papers_data.csv'
    df = pd.read_csv(CSV_FILE,encoding='mac_roman')
    data=df.iloc[:,15:16]
    
    doi_dict = altmetrics.extract_data(data)
    df = pd.DataFrame(doi_dict)
    transpose_df = df.transpose()
    transpose_df.to_csv('altmetrics.csv', encoding='utf-8')