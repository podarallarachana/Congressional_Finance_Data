# PPMemberData.py - Requests general information on members of Congress from propublica.org via API calls. 2 calls are
#                   required for each term - 1 for each chamber. Data returned in JSON format to be parsed for tables.
import json
import requests

# API Key:
PP_API_KEY = 'biZNemaKp98lNMFAYlgbP11PPYnZ6cs9WLuGyyyA'

# ProPublica URL & request info
baseReqURL = 'https://api.propublica.org/congress/v1/'
baseReqSuffix = '/members.json'
hdr = {'X-API-Key': PP_API_KEY}

# ProPublica Output file stubs
baseFileName = 'Member_List_'
baseFileNameSuffix = '.json'

# ProPublica - Get General JSON data for members of congress
for chamber in range(1, 3):
    for term in range(113, 116):
        if chamber == 1:
            urlChamber = '/house'
            fileChamber = '_House'
        else:
            urlChamber = '/senate'
            fileChamber = '_Senate'

        reqURL = baseReqURL + str(term) + urlChamber + baseReqSuffix
        print(reqURL)

        resp = requests.get(reqURL, headers=hdr)
        print('Status Code: ', resp.status_code)
        resp_json = resp.json()

        fileName = baseFileName + str(term) + fileChamber + baseFileNameSuffix
        print(fileName)

        with open(fileName, 'w') as outfile:
            json.dump(resp_json, outfile, indent=4, sort_keys=True)
