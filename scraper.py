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
for i in soup.find_all('p', style=re.compile('^.*(font-size:10.0pt;|margin:0pt 0pt 12.0pt;|text-indent:36.0pt).*$')):
    if i.find('b'):
        k = i.find('b').find('font')
        if k:
            num = None
            try:
                num = re.findall(r'\d+\.\d+',str(k.string))[0]
            except:
                num = None
            nameLetters = re.findall(r'[a-zA-Z]+',str(k.string))
            content = re.sub("<[^>]*>",'',str(i))
            if nameLetters ==[]:
                name = re.findall(r'[a-zA-Z ]+\.', content)[0]
            else:
                name = ' '.join(nameLetters)
            content = ' '.join(re.findall(r'[a-zA-Z]+', content))
            if num and name!= content:
                provision = {}
                provision= {
                'num': num.lower().lstrip(),
                'name': name.lower().lstrip(),
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
