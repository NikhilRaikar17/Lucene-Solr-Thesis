
import requests
import json
import time
from pybtex.database.input import bibtex
import pybtex.errors
import sys
pybtex.errors.set_strict_mode(False)

class ScienceDirect:

    apiKey = "8ae25cee98ba830956d895f6d2f46255"
    apiKey2 = "7f59af901d2d86f78a1fd60c1bf9426a"
    apikey3 ="6580d02a3c6cece63fd07a71153aa96e"
    newapikey ="7b234f853f17933508c848a50784125b"
    url = "https://api.elsevier.com/content/search/sciencedirect?"
    url2 = "http://api.elsevier.com/content/serial/title?"
    url3 = "https://api.elsevier.com/analytics/plumx/doi/"
    url_citation = "https://api.elsevier.com/content/abstract/citation-count?"
    url_citation2="http://api.elsevier.com/content/search/scopus?query=DOI("
    url_doi ="https://api.elsevier.com/content/search/scopus?query=title("
    url_doi_all ="https://api.elsevier.com/content/search/scopus?query=doi("
    altmetris_url = "https://api.altmetric.com/v1/doi/"

    getVars = {'apiKey': apiKey}
    getVars2 = {'apiKey': apiKey2}
    getVars3 = {'apiKey': apikey3}


    # Get citation count request new
    def getAltmetricsdata(self,lit):
        if lit is "":
            return
        if lit is None:
            return
        else:
            doi_lit = lit
            print(doi_lit)
            requestUrl = self.altmetris_url + doi_lit
            print(requestUrl)
            response = requests.get(requestUrl)
            try:
                print(response.json())
                #r = response.json()
                #print(r)
            except Exception as e:
                print(e)

# altmetrics = Altmetrics()
#                 #altmetrics.recLiterature_id = lit
#                 altmetrics.Literature_id = lit
#                 #altmetrics.altmetric_jid = data["altmetric_jid"]
#                 altmetrics.type = data["type"]
#                 altmetrics.altmetric_id = data["altmetric_id"]
#                 if "journal" in data:
#                     altmetrics.journal = data["journal"]
#                 if "is_oa" in data:
#                     altmetrics.is_oa = data["is_oa"]
#                 if "schema" in data:
#                     altmetrics.schema = data["schema"]
#                 if "score" in data:
#                     altmetrics.score = data["score"]
#                 if "cited_by_posts_count" in data:
#                    altmetrics.cited_by_posts_count = data["cited_by_posts_count"]
#                 if "cited_by_msm_count" in data:
#                    altmetrics.cited_by_msm_count = data["cited_by_msm_count"]
#                 if "cited_by_policies_count" in data:
#                    altmetrics.cited_by_policies_count = data["cited_by_policies_count"]
#                 if "cited_by_tweeters_count" in data:
#                    altmetrics.cited_by_tweeters_count = data["cited_by_tweeters_count"]
#                 if "cited_by_fbwalls_count" in data:
#                    altmetrics.cited_by_fbwalls_count = data["cited_by_fbwalls_count"]
#                 if "cited_by_rh_count" in data:
#                    altmetrics.cited_by_rh_count = data["cited_by_rh_count"]
#                 if "cited_by_patents_count" in data:
#                    altmetrics.cited_by_patents_count = data["cited_by_patents_count"]
#                 if "cited_by_accounts_count" in data:
#                    altmetrics.cited_by_accounts_count = data["cited_by_accounts_count"]
#                 if "last_updated" in data:
#                    altmetrics.last_updated = data["last_updated"]
#                 if "added_on" in data:
#                    altmetrics.added_on = data["added_on"]
#                 if "published_on" in data:
#                    altmetrics.published_on = data["published_on"]
#                 if "readers_count" in data:
#                    altmetrics.readers_count = data["readers_count"]
#                 altmetrics.citeulike_reader = data["readers"]["citeulike"]
#                 altmetrics.mendeley = data["readers"]["mendeley"]
#                 altmetrics.connotea = data["readers"]["connotea"]
#                 altmetrics.save()

#                 if "authors" in data:
#                     listofauthors = data["authors"]
#                     authorsaltmetrics = Authorsaltmetrics()
#                     authorsaltmetrics.altmetrics_id =altmetrics
#                     for k in listofauthors:
#                         authorsaltmetrics.name = k
#                         authorsaltmetrics.save()


if __name__ == "__main__":
    example = ScienceDirect()
    BIB_FILE = 'scopus_4.bib'
    bib_file = BIB_FILE
    parser = bibtex.Parser()
    bib_data = parser.parse_file(bib_file)
    for entry in bib_data.entries.values():
        doi = str(entry.fields['Doi']).replace("https://doi.org/", "")
        if doi is not None or doi!= "":
            example.getAltmetricsdata(doi)
    