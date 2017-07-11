from bs4 import BeautifulSoup
import requests
import scholarly
import re
from random import randint

class ICML2011:
    def get_papers():
        url = "http://www.icml-2011.org/papers.php"
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        papers = []
        for h2 in soup.find_all("h2"):
            cache = str(h2)
            for item in h2.find_next_siblings():
                if item.name == "h2":
                    break
                cache += str(item)
            papers.append(BeautifulSoup(cache, "html.parser"))

        filtered_papers = []

        for i in range(1,152):
            title = papers[3].select("h3")[i].text #from 0 to 151
            authors = papers[3].select("span")[i*2].text #from 0 to 302
            abstract = papers[3].select("p")[i*2+1].text #from 1 to 151
            pdf = "http://www.machinelearning.org/archive/icml2009/%s" % papers[3].select("p")[i*2].select('a')[0]['href'] #Impares
            print(pdf)
            filtered_papers.append({
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'pdf': pdf,
                'year': 2011
            })

        return filtered_papers
