from bs4 import BeautifulSoup
import requests
import scholarly
import re

template = {
    'id':'integer',
    'title':'string',
    'year':'integer',
    'authors':'array',
    'afiliation':'array',
    'citations':'integer'
}

icml = {
        "2017" : "https://2017.icml.cc/Conferences/2017/AcceptedPapersInitial"
        # "2016" : "http://icml.cc/2016/?page_id=1649",
        # "2015" : "http://proceedings.mlr.press/v37/",
        # "2014" : "http://icml.cc/2014/index/article/15.htm",
        # "2013" : "http://proceedings.mlr.press/v28/",
        # "2012" : "http://icml.cc/2012/papers/",
        # "2011" : "http://www.icml-2011.org/papers",
        # "2010" : "http://icml2010.haifa.il.ibm.com/abstracts.html"
}

def get_gscholar_info(title):
    search_query = scholarly.search_pubs_query(title)
    return next(search_query)

def extract(string, start='(', stop=')'):
        return string[string.index(start)+1:string.index(stop)]

conferences = icml.items()

soups = {}
for year, url in conferences:
    print("Getting icml year %s" % year)
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    soups[year] = soup

papers = soups["2017"]. find_all('p')

filtered_papers = []

for paper in papers:
    try:
        title = paper.find('b').get_text()
        authors = paper.find('i').get_text().split("·")
        filtered_papers.append({
            'title':title,
            'authors':authors
        })
    except:
      pass

final_papers = []

for paper in filtered_papers:
    authors = paper['authors']
    year = 2017
    try:
        citations = 0 #scholarly.search_pubs_query(title).citedby
    except:
        citations = 0

    filtered_authors = []
    afiliations = []

    for author in authors:
        filtered_authors.append(re.sub(r'\([^)]*\)', '', author))
        afiliations.append(extract(author))
        final_papers.append({
        'title': paper['title'],
        'year': 2017,
        'authors': filtered_authors,
        'afiliations': afiliations,
        'citations': citations,
    })

print(final_papers)
