# Further addition to the topics covered in "Web-Scraping with Python" workshop
# Includes looking into new urls for qualificatoin required for a particular job
# and storing in JSON format

from bs4 import BeautifulSoup
import requests as req
import csv
import json

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'} #navigator.userAgent
jsondata = {'jobs':[]}

term = input('Enter the search term: ')
want = input('Do you want the qualifications? <y/n>: ')
want = True if want == 'y' else False

html_txt = req.get(f'https://www.simplyhired.com/search?q={term}&l=',headers=headers).text
soup = BeautifulSoup(html_txt, 'lxml')
job_list = soup.find_all('div', class_='SerpJob-jobCard card') #{'class':'SerpJob-jobCard card'}

CSVfields = ['Job','Company','Location','Qualifications','Link']
CSVFile = f'simplyhired_{term}.csv'

with open(CSVFile, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(CSVfields)
    for jobs in job_list:
        name = jobs.find('a').text
        link = jobs.find('a').get('href')
        link = link.split('/')[2].split('?')[0]
        company = jobs.find('span',class_='JobPosting-labelWithIcon jobposting-company').text
        location = jobs.find('span',class_='JobPosting-labelWithIcon jobposting-location').text.replace('\u00a0',' ')
        try: 
            price = jobs.find('div',class_='jobposting-salary').text
        except:
            price = 'Not Available'

        # Job Qualification
        qualifications = []
        link = f'https://www.simplyhired.com/job/{link}'
        if want:
            html_job_detail = req.get(link,headers=headers).text
            details = BeautifulSoup(html_job_detail, 'lxml')
            for qualification in details.find_all('li',class_='viewjob-qualification'):
                qualifications.append(qualification.text)
        jsondata['jobs'].append({'Name': name,'Company': company, 'Location': location, 'Qualifications': qualifications, 'Link': link})
        writer.writerow([name,company,location,qualifications,link])
        # print(f'\nJob: {name}\nLink: {link}\nCompnay: {company}   Location: {location}\nPrice: {price}\nQualification: {qualifications}')
    
with open(f'simplyhired_{term}.json','w') as jsonfile:
    json.dump(jsondata, jsonfile, indent=2)