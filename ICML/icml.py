from bs4 import BeautifulSoup
import requests
import scholarly
import re
from random import randint
import csv
import PyPDF2

papers = []

from icml2008 import ICML2008
from icml2009 import ICML2009
from icml2010 import ICML2010
from icml2011 import ICML2011
from icml2012 import ICML2012
from icml2013 import ICML2013
from icml2014 import ICML2014
from icml2015 import ICML2015
from icml2016 import ICML2016
from helpers import Helpers

papers = ICML2008.get_papers() #+ ICML2009.get_papers() + ICML2010.get_papers() + ICML2011.get_papers() + ICML2012.get_papers() + ICML2013.get_papers()+ ICML2014.get_papers()+ ICML2015.get_papers()+ ICML2016.get_papers()

print(len(papers))

for index, paper in enumerate(papers):
    paper['reference'] = index
    print(paper)

    #Download PDF
    try:
        Helpers.download_pdf(paper['pdf'], "%i .- %s" % (index, paper['title']))
        affiliation = Helpers.get_affiliations("%i .- %s" % (index, paper['title']), paper['authors'])
    except:
        print(">>>>>>>>>>>>>> ERROR WITH PDFs <<<<<<<<<<<<<<<<<<<")
        paper['pdf'] = "ERROR ->> " + paper['pdf']
        paper['affiliation'] = "NOT FOUND"


    if not "affiliation" in paper:
        paper['affiliation'] = affiliation
