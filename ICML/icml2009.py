from bs4 import BeautifulSoup
import requests
import scholarly
import re
from random import randint


class ICML2009(object):
    def get_papers():
        url = "http://www.machinelearning.org/archive/icml2009/abstracts.html"

        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        papers = []
        for hr in soup.find_all("hr"):
            cache = ""
            for item in hr.find_next_siblings():
                if item.name == "hr":
                    break
                cache += str(item)
            papers.append(BeautifulSoup(cache, "html.parser"))

        filtered_papers = []

        for paper in papers:
            title = paper.h3.text
            authors = paper.p.text
            abstract = paper.select('p')[2].text
            pdf = "http://www.machinelearning.org/archive/icml2009/%s" % paper.select("a")[1]['href']
            filtered_papers.append({
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'pdf': pdf,
                'year': 2009
            })

        return filtered_papers
