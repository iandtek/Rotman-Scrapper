import csv
import requests

csvfilename="ICML2010.csv"
# csvfilename = input("Please enter CSV File: ")

with open(csvfilename) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        url = row[6]
        print("Downloading %s ..." % row[0])
        response = requests.get(url)

        with open("PDF/%s.pdf" % (row[0]), 'wb') as f:
            f.write(response.content)
