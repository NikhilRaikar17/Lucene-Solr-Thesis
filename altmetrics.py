from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
from pybtex.database.input import bibtex
import pybtex.errors
import sys
pybtex.errors.set_strict_mode(False)


## Initialize client
client = ElsClient("25a76f4e439ef1cb5dd7173dfb56fcac")

BIB_FILE = 'data/scopus_6.bib'

def bib_file_parser():
    bib_file = BIB_FILE
    parser = bibtex.Parser()
    bib_data = parser.parse_file(bib_file)
    for entry in bib_data.entries.values():
        doi = str(entry.fields['Doi']).replace("https://doi.org/", "")
        doi_doc = FullDoc(doi = doi)
        if doi_doc.read(client):
            print ("doi_doc.title: ", doi_doc.title)
            doi_doc.write()   
        else:
            print ("Read document failed.")


if __name__ == "__main__":
    bib_file_parser()