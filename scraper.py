from lxml import html
import requests
from bs4 import BeautifulSoup
import re
import xlsxwriter

workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()
c = open('contract.html')
S = c.read()
soup = BeautifulSoup(S, 'html.parser')

provisions = []
for i in soup.find_all('p', style=re.compile('^.*(font-size|margin|text-indent).*$')):
    content = re.sub("<[^>]*>",'',str(i))
    name = None
    bold = 'false'
    underscore = 'false'
    try:
        name = re.findall(r'[a-zA-Z ]+\.', content)[0]
    except:
        name = None
    num = None
    try:
        num = re.findall(r'\d+\.\d*',content)[0]
    except:
        num = None
    if i and i.b:
        bold = 'true'
    if i and re.findall(r'^.*(underline).*$', str(i)):
        underscore = 'true'
    content = ' '.join(re.findall(r'[a-zA-Z]+', content))
    if num and name and name!= content:
        provision = {}
        provision= {
        'num': num.lower().lstrip(),
        'name': name.lower().lstrip(),
        'bold': bold,
        'underscore': underscore,
        'content':  content.lower().lstrip(),
        }
        provisions.append(provision)
row = 0
# Iterate over the data and write it out row by row.
for p in provisions:
    col = 0
    for i in p:
        worksheet.write(row, col,p[i])
        col+=1
    row += 1
