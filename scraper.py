from lxml import html
import requests
from bs4 import BeautifulSoup
import re
import urllib.request


'''
input: String url
output: List<List>

Using the url to get the html codes and using BeautifulSoup to scrap the
information of the contract
'''
def extractAllProvision(url):

    # Reading the url and get html content
    fp = urllib.request.urlopen(url)
    htmlBytes = fp.read()
    htmlStr = htmlBytes.decode("utf8")

    # processing the content using BeautifulSoup
    soup = BeautifulSoup(htmlStr, 'html.parser')

    # Get the contract content according to the class
    contract = soup.find('div', {'class': 'row contract-content'})
    content = contract.div.div
    children = content.findChildren()


    # start to Iterate provisions
    provisions = []
    num = 1
    name = ''
    for child in children:
        childContent = re.sub("<[^>]*>",'',str(child)).strip()
        if len(childContent)>2:

            # if it has bold or underscore
            bold = False
            underscore = False
            if child.b:
                bold = True
            if child.u:
                underscore = True

            # try to get the name and index of the provision
            currnum = 0.5
            currname = ''
            try:
                currnum = float(re.findall(r'\d+\.\d*',childContent[0:10])[0].lstrip())
                try:
                    currname = child.u.string
                except:
                    currname = re.findall(r'[a-zA-Z ]+\.', childContent)[0]
                num = currnum
                name = currname

            except:
                currnum = num
                currname = name

            # Get the content of the provision
            provisionContent = ' '.join(re.findall(r'[a-zA-Z]+', childContent)).strip()

            # put this provision in the list
            if provisionContent:
                provision= [
                currnum,currname.lstrip(),bold,underscore, provisionContent.lower().lstrip(),
                ]
                provisions.append(provision)

    # remove duplicates
    cleanProvisions = []
    numCache = 0.5
    nameCache = ''
    contentCache = ''
    for i in range(0, len(provisions)):
        # remove the duplicates according to the name and content
        if provisions[i][1] ==provisions[i][-1] or provisions[i][0] == 0.5:
            continue
        if len(cleanProvisions)>0 and provisions[i][0] == numCache and provisions[i][-1] == contentCache:
            continue

        if provisions[i][0]!= numCache:
            cleanProvisions.append(provisions[i])
            numCache = provisions[i][0]

        if len(cleanProvisions)>0 and provisions[i][0] == numCache and provisions[i][-1] != contentCache:
            #cleanProvisions.append((provisions[i][0], provisions[i][1], provisions[i][2], provisions[i][3], cleanProvisions))
            cleanProvisions[-1][-1] += provisions[i][-1]
            contentCache = provisions[i][-1]


    return cleanProvisions

'''
input: List<List>
output: Boolean
return if the contract has subprovisions
'''
def hasSubProv(provisions):
    count = 0
    for i in range(0, len(provisions)):
        if provisions[i][0] - float(int(provisions[i][0])) == 0.0:

            # if i> half of the size of the provisions, it means this is not a mainprovision index
            if i> len(provisions)/2:
                return False
            count += 1
    return count > 3

'''
input: List<List>
output: List<List>
Combine subprovision together.
'''
def cleanSubProvisions(provisions):
    result = []
    if hasSubProv(provisions):
        noSubProvisions = []
        subTitle = 0.0
        for i in range(0, len(provisions)):
            if provisions[i][0] - float(int(provisions[i][0])) == 0.0:
                subTitle = provisions[i][0]
                result.append(provisions[i])
            if provisions[i][0] - subTitle < 1.0:
                result[-1][-1] += provisions[i][-1]
        return result
    else:
        return provisions




def extractOneProvision(url, provisionName):
    pass
