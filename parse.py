from bs4 import BeautifulSoup
import requests
import unicodecsv
import argparse
import sys


def valid_conference(s):
    """Convert conference string into a valid format (lowercaseYYYY)"""
    s = s.lower()
    if s[-4:].isdigit() and s[:-4].isalpha():
        return s.lower()
    else:
        raise ValueError('Conference format must be in [a-z]YYYY e.g. cvpr2015')


def rank_authors(authors):
    """Simple generator to take a list of authors and return a tuple with their ranks.
    Rank: 1 - first author, 2 - contributing author, 3 - last author
    Use it like the built-in enumerate.
    """
    for i, author in enumerate(authors):
        if i == 0:
            rank = 1
        elif i == (len(authors) - 1):
            rank = 3
        else:
            rank = 2
        yield rank, author


def parse_cvfoundation(conference):
    """
    Parse a CV-Foundation conference URL.
    e.g. 'cvpr2016' -> http://www.cv-foundation.org/openaccess/CVPR2016.py
    """
    base_url = 'http://www.cv-foundation.org/openaccess/'
    url = base_url + conference.upper() + '.py'
    print("Connecting to URL: %s" % url)
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    dt_list = soup.find_all("dt")
    dd_list = soup.find_all("dd")
    print("Found %d papers." % (len(dt_list) / 2))
    for dt, dd_author, dd_pdf in zip(dt_list, dd_list[0::2], dd_list[1::2]):
        title = dt.string
        abstract_url = base_url + dt.find('a')['href']
        paper_url = base_url + dd_pdf.find('a')['href']
        authors = [x['value'] for x in dd_author.find_all('input')]
        entry = {
            'title': title,
            'abstract_url': abstract_url,
            'paper_url': paper_url,
            'authors': authors
        }
        yield entry


def parse_cvpapers(conference):
    base_url = 'http://www.cvpapers.com/'
    url = base_url + conference.lower() + ".html"
    print("Connecting to URL: %s" % url)
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    dt_list = soup.find_all('dt')  # Title and paper url
    dd_list = soup.find_all('dd')  # Author
    assert len(dt_list) == len(dd_list)
    print("Found %d papers." % len(dt_list))
    for dt, dd in zip(dt_list, dd_list):
        authors = [x.strip() for x in dd.text.replace('\n', ' ').replace(' and ', ',').split(',') if x.strip()]
        title = dt.text.rsplit('(')[0].replace('\n', ' ')
        paper_url = dt.find('a', text='PDF')
        if paper_url:
            paper_url = paper_url['href']
        entry = {
            'title': title,
            'paper_url': paper_url,
            'authors': authors
        }
        yield entry


def parse_icml2016(conference):
    assert conference == 'icml2016'
    url = 'http://icml.cc/2016/?page_id=1649'
    print("Connecting to URL: %s" % url)
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    papers = soup.find('div',{'id':'schedule'}).find_all('li')

    for paper in papers:
        title = paper.find('span', {'class':'titlepaper'}).text
        authors = []
        institutions = []
        for x in paper.find('span', {'class':'authors'} ).children:
            if x.name == 'i':
                institutions.append( x.text.strip() )
            else:
                authors.append( x.replace(',','').strip() )
        assert len(authors) == len(institutions)
        entry = {
            'title' : title,
            'authors' : authors,
            'institutions' : institutions
        }
        yield entry



def parse_jmlr(conference):
    url_lookup = {
        'icml2013': 'http://jmlr.csail.mit.edu/proceedings/papers/v28/',
        'icml2014': 'http://jmlr.csail.mit.edu/proceedings/papers/v32/',
        'icml2015': 'http://jmlr.csail.mit.edu/proceedings/papers/v37/',
    }
    url = url_lookup[conference]
    print("Connecting to URL: %s" % url)
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    papers = soup.find_all('div', {'class': 'paper'})
    print("Found %d papers." % len(papers))
    for paper in papers:
        title = paper.find('', {'class': 'title'}).text
        authors = [x.strip() for x in paper.find('', {'class': 'authors'}).string.split(',')]
        abstract_url = paper.find('a', text='abs')
        paper_url = paper.find('a', text='pdf')
        if abstract_url:
            abstract_url = abstract_url['href']
        if paper_url:
            paper_url = paper_url['href']
        entry = {
            'title': title,
            'paper_url': paper_url,
            'abstract_url': abstract_url,
            'authors': authors
        }
        yield entry


def parse_nips(conference):
    year = int(conference[-4:])
    no = year - 1987
    base_url = 'https://papers.nips.cc'
    url = base_url + '/book/advances-in-neural-information-processing-systems-%d-%d' % (no, year)
    print("Connecting to URL: %s" % url)
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    papers = [x for x in soup.find_all('li') if x.find('', {'class': 'author'})]
    print("Found %d papers." % len(papers))
    for paper in papers:
        title = paper.find('a').text
        abstract_url = base_url + paper.find('a')['href']
        authors = [x.text for x in paper.find_all('a', {'class': 'author'})]
        paper_url = abstract_url + ".pdf"
        entry = {
            'title': title,
            'abstract_url': abstract_url,
            'paper_url': paper_url,
            'authors': authors
        }
        yield entry


def parse(conference):
    if 'icml' in conference:
        if conference == 'icml2016':
            return parse_icml2016(conference)
        else:
            return parse_jmlr(conference)
    elif ('cvpr' in conference and conference >= 'cvpr2013') or ('iccv' in conference and conference >= 'iccv2013'):
        return parse_cvfoundation(conference)
    elif ('cvpr' in conference and conference >= 'cvpr2007') or \
            ('eccv' in conference and conference >= 'eccv2006'):
        return parse_cvpapers(conference)
    elif 'nips' in conference:
        return parse_nips(conference)
    else:
        raise ValueError("No parser available for conference: %s" % conference)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Scrape the web to extract machine learning papers and authors.')
    parser.add_argument('--output', type=str, default=None, help='Path to parsed list of authors')
    parser.add_argument('conference', type=valid_conference, help='Conference to target in [a-z]YYYY format. e.g. cvpr2016')

    args = parser.parse_args()
    if args.output is None:
        args.output = args.conference + '.csv'

    output_fields = ["author", "rank", "title", "abstract_url", "paper_url", "institution"]
    with open(args.output, 'wb') as fout:
        csv_writer = unicodecsv.DictWriter(fout, output_fields, encoding='utf-8')
        csv_writer.writeheader()
        for entry in parse(args.conference):
            authors = entry.pop('authors')
            institutions = entry.pop('institutions', [None]*len(authors))
            for rank, (author, institution) in rank_authors( list(zip(authors, institutions))):
                entry['rank'] = rank
                entry['author'] = author
                entry['institution'] = institution
                csv_writer.writerow(entry)
    print("Output written to: %s" % args.output)
