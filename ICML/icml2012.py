from bs4 import BeautifulSoup
import requests

class ICML2012:
    def get_papers():
        url = "http://icml.cc/2012/papers/"

        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        papers = soup.select(".paper")

        filtered_papers = []
        final_papers = []

        for paper in papers:
            title = paper.h2.text
            authors = paper.p.text.split('\r\n', 1)[0]
            abstract = paper.select(".abstract")[0].text.split("\n")[0]
            try:
                pdf = "http://icml.cc/2012/papers/%s" % paper.select("a")[1]['href']
            except:
                pdf = "No PDF Found"
            filtered_papers.append({
                'title':title,
                'authors':authors,
                'abstract':abstract,
                'pdf':pdf,
                'year': 2012
            })


        return filtered_papers
