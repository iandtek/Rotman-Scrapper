from bs4 import BeautifulSoup
import requests
import scholarly
import re

url = "http://icml2010.haifa.il.ibm.com/abstracts.html"

def extract(string, start='(', stop=')'):
        return string[string.index(start)+1:string.index(stop)]


soup = BeautifulSoup(requests.get(url).content, "html.parser")
titles = soup.find_all('h3')

for _ in range(4):
    titles.pop(0)

authors_with_afiliation = soup.find_all('em')


filtered_papers = []
final_papers = []

for index,title in enumerate(titles):
    title = title.get_text()
    authors = authors_with_afiliation[index].get_text().split(";")
    filtered_papers.append({
        'title':title,
        'authors':authors
    })

for paper in filtered_papers:
    authors = paper['authors']
    year = 2017

    filtered_authors = []
    afiliations = []

    for author in authors:
        filtered_authors.append(re.sub(r'\([^)]*\)', '', author))
        afiliations.append(extract(author))

    try:
        query = "%s" % (paper['title']) #, ','.join(filtered_authors)
        print(query)
        g_scholar = next(scholarly.search_pubs_query(query))
        citations = g_scholar.citedby
    except:
        citations = 0

    print("%s : %s" % (paper['title'], citations) )

    final_papers.append({
        'title': paper['title'],
        'year': 2017,
        'authors': filtered_authors,
        'afiliations': afiliations,
        'citations': citations,
    })

print(final_papers)
