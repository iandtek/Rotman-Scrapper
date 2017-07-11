from bs4 import BeautifulSoup
import requests

class ICML2014:
    def get_abstract(url):
        try:
            soup = BeautifulSoup(requests.get(url).content, "html.parser")
            abstract = soup.select(".abstract")[0].text.replace("\n","")
        except:
            abstract = "Not Found"
        return abstract

    def get_papers():
        url = "http://icml.cc/2014/index/article/15.htm"

        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        papers = soup.select("dl")

        filtered_papers = []

        for paper in papers:
            title = paper.dt.text
            authors = paper.dd.text
            abstract = ICML2014.get_abstract(paper.select("a")[0]['href'])
            pdf = paper.select("a")[1]['href']
            filtered_papers.append({
                'title':title,
                'authors':authors,
                'abstract':abstract,
                'pdf':url + pdf,
                'year':2014
            })
        return filtered_papers
