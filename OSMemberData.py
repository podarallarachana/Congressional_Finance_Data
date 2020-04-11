# OSMemberData.py - Retrieves .xml data using 4 different APIs from opensecrets.org. Uses 3 different API keys (one per
#                   person working on the project) as there is a limit of 200 calls per API per key per day. Because of
#                   this limit, this file will be updated daily (reflected in the 'for i in range(x, y)' statements)
#                   until all data is retrieved. There are approximately 700 CRP IDs to be used for retrieval overall.
import json
import requests
from lxml import etree

# API Keys:
OS_API_KEY_1 = '8e93f4f2ba901e97d2a5a6efad6827f7'
OS_API_KEY_2 = 'df03037bb09cca6476b25df5b7c84a67'
OS_API_KEY_3 = '0da28a05ff606b574ec9e5df9c741618'

# Open Secrets API keys in list form for use in loops
OS_API_KEYS = [OS_API_KEY_1, OS_API_KEY_2, OS_API_KEY_3]

### URLs for API calls ###
# Insert cid after the following
pfdReqUrl1 = 'http://www.opensecrets.org/api/?method=memPFDprofile&year=2016&cid='
# Insert this part after cid, then insert API key
pfdReqUrl2 = '&output=xml&apikey='

# Insert cid after the following
candSumReqUrl1 = 'http://www.opensecrets.org/api/?method=candSummary&cid='
# Then insert this followed by election cycle
candSumReqUrl2 = '&cycle='
# Insert after election cycle year, then insert API key
candSumReqUrl3 = '&apikey='

# Insert cid after the following
candIndReqUrl1 = 'http://www.opensecrets.org/api/?method=candIndustry&cid='
# Then insert this followed by election cycle
candIndReqUrl2 = '&cycle='
# Insert after election cycle year, then insert API key
candIndReqUrl3 = '&apikey='

# Insert cid after the following
candSectReqUrl1 = 'http://www.opensecrets.org/api/?method=candSector&cid='
# Then insert this followed by election cycle
candSectReqUrl2 = '&cycle='
# Insert after election cycle year, then insert API key
candSectReqUrl3 = '&apikey='

# Election cycles relevant to data (113th, 114th, 115th Congressional terms)
cycles = ['2012', '2014', '2016']

# Creates a list of all relevant CRP IDs from cross reference JSON. Each API call requires a single CRP ID.
pathToCR = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\ppGeneralInfo\\CR.json'
crList = []
with open(pathToCR) as jsonFile:
    crData = json.load(jsonFile)
for key, value in crData.items():
    crList.append(value['crp_Id'])

# Retrieve member profile data for each CRP ID. Each member has their own XML file.
pfdBasePath = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\memPFDprofile\\'
for i in range(450, 600):
    respUrl = pfdReqUrl1 + crList[i] + pfdReqUrl2 + OS_API_KEYS[0]
    resp = requests.get(respUrl)
    if resp.status_code == 200:
        root = etree.fromstring(resp.text)
        tree = etree.ElementTree(root)
        filePath = pfdBasePath + crList[i] + '_memPFD.xml'
        tree.write(filePath, pretty_print=True)
    else:
        print('PfdResp' + str(i) + ': ' + str(resp.status_code) + '(crp_id: ' + crList[i] + ')')

# Retrieve candidate summary data for each CRP ID and cycle. For each year that data exists for a given CRP ID, an XML
# file is created and saved to a folder named for that cycle.
candSumBasePath = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\candSummary\\'
for i in range(450, 600):
    for j in range(0, 3):
        respUrl = candSumReqUrl1 + crList[i] + candSumReqUrl2 + cycles[j] + candSumReqUrl3 + OS_API_KEYS[j]
        resp = requests.get(respUrl)
        if resp.status_code == 200:
            root = etree.fromstring(resp.text)
            tree = etree.ElementTree(root)
            filePath = candSumBasePath + str(cycles[j]) + '\\' + crList[i] + '_candSum.xml'
            tree.write(filePath, pretty_print=True)
        else:
            print('CSumResp' + str(i) + ': ' + str(resp.status_code) + '(crp_id: ' + crList[i] + ', year: ' + str(cycles[j]) + ')')

# Retrieve candidate industry data for each CRP ID and cycle. For each year that data exists for a given CRP ID, an XML
# file is created and saved to a folder named for that cycle.
candIndBasePath = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\candIndustry\\'
for i in range(450, 600):
    for j in range(0, 3):
        respUrl = candIndReqUrl1 + crList[i] + candIndReqUrl2 + cycles[j] + candIndReqUrl3 + OS_API_KEYS[j]
        resp = requests.get(respUrl)
        if resp.status_code == 200:
            root = etree.fromstring(resp.text)
            tree = etree.ElementTree(root)
            filePath = candIndBasePath + str(cycles[j]) + '\\' + crList[i] + '_candInd.xml'
            tree.write(filePath, pretty_print=True)
        else:
            print('CIndResp' + str(i) + ': ' + str(resp.status_code) + '(crp_id: ' + crList[i] + ', year: ' + str(cycles[j]) + ')')

# Retrieve candidate sector data for each CRP ID and cycle. For each year that data exists for a given CRP ID, an XML
# file is created and saved to a folder named for that cycle.
candSectBasePath = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\candSector\\'
for i in range(450, 600):
    for j in range(0, 3):
        respUrl = candSectReqUrl1 + crList[i] + candSectReqUrl2 + cycles[j] + candSectReqUrl3 + OS_API_KEYS[j]
        resp = requests.get(respUrl)
        if resp.status_code == 200:
            root = etree.fromstring(resp.text)
            tree = etree.ElementTree(root)
            filePath = candSectBasePath + str(cycles[j]) + '\\' + crList[i] + '_candSect.xml'
            tree.write(filePath, pretty_print=True)
        else:
            print('CSecResp' + str(i) + ': ' + str(resp.status_code) + '(crp_id: ' + crList[i] + ', year: ' + str(cycles[j]) + ')')
