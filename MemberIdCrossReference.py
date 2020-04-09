# MemberIdCrossReference.py - designed to create a comprehensive cross reference between Congressional members'
#                             BioGuide IDs, CRP IDs and first and last names. Because availability of data is a mixed
#                             bag, and the time to examine and parse through many sources is impractical, manual entry
#                             of a large number of CRP IDs is required. User will be prompted to provide when necessary.
import json

# Create bioguide / crp cross-reference for each member in 113-115 terms
pathToFile1 = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\ppGeneralInfo\\Member_List_115_House.json'
pathToFile2 = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\ppGeneralInfo\\Member_List_115_Senate.json'
pathToFile3 = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\ppGeneralInfo\\Member_List_114_House.json'
pathToFile4 = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\ppGeneralInfo\\Member_List_114_Senate.json'
pathToFile5 = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\ppGeneralInfo\\Member_List_113_House.json'
pathToFile6 = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\ppGeneralInfo\\Member_List_113_Senate.json'
pathsToFiles = [pathToFile1, pathToFile2, pathToFile3, pathToFile4, pathToFile5, pathToFile6]
pathToCR = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\ppGeneralInfo\\CR.json'

# Create list for entries
members = {}

# For each json file, open and load into curData -> curMembers
for paths in pathsToFiles:
    with open(paths) as file:
        curData = json.load(file)
        curMembers = curData['results'][0]['members']

        # For each entry in the file, grab the first name, last name, bioguide ID and crp ID
        for entry in curMembers:
            if 'id' not in entry:
                bioGuideId = ''
                print("BioGuideID missing from " + entry['last_name'] + ", " + entry['first_name'])
            else:
                if entry['id'] in members:
                    continue
                else:
                    bioGuideId = entry['id']
                    if bioGuideId is None:
                        print("BioGuideID missing from " + entry['last_name'] + ", " + entry['first_name'])
            if 'last_name' not in entry:
                lastName = ''
                print("Last name missing from an entry")
            else:
                lastName = entry['last_name']
                if lastName is None:
                    print("Last name missing from an entry")
            if 'first_name' not in entry:
                firstName = ''
                print("First name missing from an entry")
            else:
                firstName = entry['first_name']
                if firstName is None:
                    print("First name missing from an entry")
            if 'crp_id' not in entry:
                crpId = ''
                print("CRP_ID missing from " + entry['last_name'] + ", " + entry['first_name'])
            else:
                crpId = entry['crp_id']
                # Since checks would be time-consuming to implement, manually add crp_id from cross reference if not in data
                # Theoretically possible to have multiple people with same name from same state
                if crpId is None:
                    while (crpId is None) or (len(crpId) != 9):
                        crpId = input("Enter CRP ID for " + entry['last_name'] + ", " + entry['first_name'] + " of " + entry['state'] + ": ")
                        for key, value in members.items():
                            if crpId == value['crp_Id']:
                                print('Record already exists using ' + crpId + ' for ' + value['first_name'] + ' ' + value['last_name'] + '. Check value and try again')
                                crpId = 'X000'

            # Add entry to dictionary using bioGuideId as key
            members[bioGuideId] = {
                "last_name": lastName,
                "first_name": firstName,
                "crp_Id": crpId
            }

# Dump dictionary to json file
with open(pathToCR, 'w') as outfile:
    json.dump(members, outfile, indent=4, sort_keys=True)
