# Complete code from the "Web-Scraping with Python Workshop"

from bs4 import BeautifulSoup
import requests
import csv

search = input('Enter the search term: ')

CSVFields = ['name','company','salary']
file = f'{search}.csv'

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'}
html_text = requests.get(f'https://www.simplyhired.com/search?q={search}&l=',headers=headers).text

soup = BeautifulSoup(html_text,'lxml')

jobs = soup.find_all('div',class_='SerpJob-jobCard card')

with open(file,'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(CSVFields)
    for job in jobs:
        job_name = job.find('a').text
        company = job.find('span',class_='JobPosting-labelWithIcon jobposting-company').text
        location=job.find('span',class_='JobPosting-labelWithIcon jobposting-location').text
        try:
            salary = job.find('div',class_='jobposting-salary').text
        except:
            salary='Not Available'
        writer.writerow([job_name,company,salary])