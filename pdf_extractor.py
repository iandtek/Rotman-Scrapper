import PyPDF2
import csv
import requests
import re

csvfilename="ICML2010.csv"
# csvfilename = input("Please enter CSV File: ")

data = []

def read_pdf(location):
    pdfFileObj = open(location, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)
    text = pageObj.extractText().split("Abstract")[0] #Extract before the title Abstract
    return text

def camel2normal(string):
    return re.sub("([a-z])([A-Z])","\g<1> \g<2>",string).replace("of ", " of ").replace("and ", " and ").replace("for ", " for ")

with open(csvfilename) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        data.append(row)


for i in range(7, 40):
    print("*******************************************************\n\n")
    print("%s.pdf" % data[i+1][1])
    authors = eval(data[i+1][4])
    print("Authors: %s" % authors )
    pdf_text = read_pdf("PDF/%s.pdf" % data[i+1][1])
    # print(pdf_text)
    raw_text = pdf_text.split("\n")
    list_sorted = sorted(raw_text, key=len)[::-1]

    for author in authors:
        list_sorted = [ x for x in list_sorted if author.split(" ")[1] not in x ] #Remove Authors

    list_sorted = [ x for x in list_sorted if "@" not in x ] #remove emails

    list_sorted = [ x for x in list_sorted if data[i+1][1].split(" ")[0] not in x ] #Remove Title
    list_sorted = [ x for x in list_sorted if data[i+1][1].split(" ")[-1] not in x ] #Remove Title
    filtered = []
    for string in list_sorted:
        if len(string) > 20:
            if string[0].isupper():
                filtered.append(string)

    affiliation = [x for x in raw_text if x in filtered]
    affiliation = list(map(camel2normal, affiliation))
    print(affiliation)
