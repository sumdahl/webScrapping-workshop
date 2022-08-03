# Extra addition to "Web-Scraping with Python" workshop
# Involves scraping timesjobs.com
# Involves scraping and filtering of data and the use of functions

from bs4 import BeautifulSoup
import requests as req

def showlist(list):
    for elements in list:
        print(elements)

def showcase(companys, skills, details, posted):
    for company,skill,detail,date in zip(companys,skills,details,posted):
        print(f'''\nCompany Name: {company}\nSkills Required: {skill}\nDetails: {detail}\n{date}''')

def writeout(index,name,skill,detail,date):
    with open(f"job{index}.txt", 'w') as file:
        file.write(f"Company Name: {name}\nSkills Required: {skill}\nDetails: {detail}\n{date}")

search = input('Enter the search term: ')
html_txt = req.get(f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={search}+&txtLocation=').text
soup = BeautifulSoup(html_txt, 'lxml')
job_list = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

company_names = []
skills = []
details = []
posted = []

inp = input('Skills to search for: <seperate skills with only ,> \n')
inp = inp.split(',')

for i,jobs in enumerate(job_list):
    date = jobs.find('span', class_='sim-posted').text.replace('\n','')
    skill = (jobs.find('span', class_='srp-skills').text.replace('\r\n','').replace('  ','').replace('\n','')).split(',')
    if(date=='Posted few days ago'):
        satisfied = all(s in skill for s in inp)
        if satisfied:
            name = jobs.find('h3', class_='joblist-comp-name').text.replace(' ','').replace('\r\n','')
            detail = jobs.header.h2.a['href']
            
            company_names.append(name)
            skills.append(skill)
            details.append(detail)
            posted.append(date)

            writeout(i,name,skill,detail,date)

showcase(company_names,skills,details,posted)