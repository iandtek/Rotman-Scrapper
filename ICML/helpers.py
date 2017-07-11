from bs4 import BeautifulSoup
import requests
import scholarly
import re
from random import randint
import csv
import PyPDF2
from difflib import SequenceMatcher

class Helpers:
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def get_citations(query):
        try:
            print("Getting Citations from Google Scholar...")
            g_scholar = next(scholarly.search_pubs_query(query))
            citations = g_scholar.citedby
            print(g_scholar)
            # citations = randint(0, 777)
        except:
            citations = "null"
        return citations

    def download_pdf(url, name):
        print("Downloading %s ..." % url)
        try:
            response = requests.get(url)
            with open("PDF/%s.pdf" % (name), 'wb') as f:
                f.write(response.content)
            result = 0
        except:
            print("Error")
            result = -1
        return result

    def read_pdf(location):
        pdfFileObj = open(location, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0)
        text = pageObj.extractText().split("Abstract")[0] #Extract before the title Abstract
        return text

    def camel2normal(string):
        return re.sub("([a-z])([A-Z])","\g<1> \g<2>",string).replace("of ", " of ").replace("and ", " and ").replace("for ", " for ").replace(",", ", ")

    def get_affiliations(title, authors):
        pdf_text = Helpers.read_pdf("PDF/%s.pdf" % title)
        raw_text = pdf_text.split("\n")
        list_sorted = sorted(raw_text, key=len)[::-1]
        authors = authors.split(" ")
        for author in authors:
            list_sorted = [ x for x in list_sorted if author not in x ] #Remove Authors
        list_sorted = [ x for x in list_sorted if "@" not in x ] #remove emails

        arr_title = title.split(" ")
        list_sorted = [ x for x in list_sorted if arr_title[0] not in x ] #Remove Title
        # list_sorted = [ x for x in list_sorted if arr_title[-1] not in x ] #Remove Title
        # list_sorted = [ x for x in list_sorted if arr_title[int(len(arr_title)/2)] not in x ] #Remove Title
        filtered = []
        for string in list_sorted:
            if len(string) > 30:
                if string[0].isupper():
                    if not Helpers.similar(string, title) > 0.5:
                        filtered.append(string)

        affiliation = [x for x in raw_text if x in filtered]
        affiliation = list(map(Helpers.camel2normal, affiliation))
        print("$#####################")
        for item in affiliation:
            print(item)    
        return affiliation
