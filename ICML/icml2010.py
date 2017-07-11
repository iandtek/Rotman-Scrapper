from bs4 import BeautifulSoup
import requests
import scholarly
import re
from random import randint

class ICML2010(object):
    url = "http://icml2010.haifa.il.ibm.com/abstracts.html"

    def extract(string, start='(', stop=')'):
        try:
            string = string[string.index(start)+1:string.index(stop)]
        except:
            pass
        return string
    def get_papers():
        print("Getting HTML")
        soup = BeautifulSoup(requests.get(ICML2010.url).content, "html.parser")
        titles = soup.find_all('h3')
        abstracts = soup.select('.abstracts')
        pdfs = soup.select('.discussion')

        for _ in range(4):
            titles.pop(0)

        authors_with_afiliation = soup.find_all('em')


        filtered_papers = []
        final_papers = []

        for index,title in enumerate(titles):
            title = title.get_text()
            authors = authors_with_afiliation[index].get_text().split(";")
            abstract = abstracts[index].text
            pdf = pdfs[index].a['href']
            filtered_papers.append({
                'title':title,
                'authors':authors,
                'abstract':abstract,
                'pdf': pdf
            })

        for index, paper in enumerate(filtered_papers):
            authors = paper['authors']
            year = 2010

            filtered_authors = []
            afiliations = []

            for author in authors:
                filtered_authors.append(re.sub(r'\([^)]*\)', '', author))
                afiliations.append(ICML2010.extract(author))

            final_papers.append({
                'title': paper['title'],
                'abstract': paper['abstract'],
                'year': 2010,
                'authors': ''.join(filtered_authors).replace("  ", ", "),
                'affiliation': ', '.join(afiliations),
                'pdf': "http://icml2010.haifa.il.ibm.com/%s" % paper['pdf']
            })
            print(final_papers[::-1])

        return final_papers
