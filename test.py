from scraper import extractAllProvision,cleanSubProvisions
import xlsxwriter

provs = cleanSubProvisions(extractAllProvision('https://www.lawinsider.com/contracts/50EkUcDbOfMwYQ3lvmZj5j/tandem-diabetes-care/delaware/2013-11-04'))
workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()
row = 0
for p in provs:
    col = 0
    for i in p:
        worksheet.write(row, col, i)
        col+=1
    row += 1
