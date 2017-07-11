from bs4 import BeautifulSoup
import requests

class ICML2008:
    def get_papers():
        url = "http://www.machinelearning.org/archive/icml2008/abstracts.shtml"
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
            try:
                title = paper.h3.text
                authors = paper.i.text
                abstract = paper.select('p')[2].text
                pdf = "http://www.machinelearning.org/archive/icml2009/%s" % paper.select("a")[1]['href']
                filtered_papers.append({
                    'title': title,
                    'authors': authors,
                    'abstract': abstract,
                    'pdf': pdf,
                    'year': 2008
                })
            except:
                pass
        return filtered_papers
