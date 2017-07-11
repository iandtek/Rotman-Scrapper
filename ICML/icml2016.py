from bs4 import BeautifulSoup
import requests
import scholarly
import re
from random import randint

class ICML2016:
    def get_abstract(url):
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        abstract = soup.select(".abstract")[0].text
        return abstract.replace("\n","")

    def get_papers():
        url = "http://proceedings.mlr.press/v48/"

        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        papers = soup.select(".paper")
        filtered_papers = []
        for paper in papers:
            title = paper.select(".title")[0].text
            authors = paper.select(".authors")[0].text.replace("      ","").replace("\n","")
            abstract = ICML2016.get_abstract(paper.select("a")[0]['href'])
            pdf = paper.select("a")[1]['href']
            filtered_papers.append({
                'title':title,
                'authors':authors,
                'abstract':abstract,
                'pdf':url + pdf,
                'year':2016
            })
        return filtered_papers
