from bs4 import BeautifulSoup as bs
import requests
import csv

# add URL of search site here
URL = "https://studentjobs.seo.cornell.edu/jobpostings?term=100&region=any&employertype=any&field=any&extra=1&criteria="
page = requests.get(URL)
master_site = bs(page.content, "html.parser")

labels = []
first = True

info = []

for i in master_site.find_all(class_="mobile-right"):
    search_link = "https://studentjobs.seo.cornell.edu/" + i.a.get("href")
    search_site = bs(requests.get(search_link).content, "html.parser")

    if first:
        labels = [j.text for j in search_site.find_all(class_="field-label")]

    info.append([j.text for j in search_site.find_all(class_="field-data")])

    first = False

print("Processing finished.")

with open("jobs.tsv", 'w', encoding='utf-8', newline='') as tsvfile:
    writer = csv.writer(tsvfile, delimiter="\t")
    writer.writerow(labels)
    for i in info:
        writer.writerow(i)

print("Writing finished.")