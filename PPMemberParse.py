# PPMemberParse.py - Parses JSON data retrieved from propublica.org containing general information on members of
#                    Congress. Since information can be in multiple locations (e.g., the data of a representative that
#                    served in both the 114th and 115th terms will be listed in the JSON files for both terms), the
#                    parsing is done in reverse date order with only the first data found on a member saved to the csv
import os
import json
import csv
from pathlib import Path

# Change directory based on data files location. As long as files are at or below this
# level and have the proper file name (-e.json), they will be parsed.
baseDir = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\ppGeneralInfo'
pwdPath = Path(__file__)

# Pull in bioguide->crp ID cross reference. Create dictionary that maps bioguide ID to crp ID
pathToCR = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\ppGeneralInfo\\CR.json'
BioToCrp = {}
with open(pathToCR) as jsonFile:
    crData = json.load(jsonFile)
for key, value in crData.items():
    BioToCrp[key] = value['crp_Id']

# CSV filenames and headers
memberInfoFileName = (pwdPath / '../csv/MemberInfo.csv').resolve()
memberInfoHeader = ['bioguide_id', 'crp_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'party', 'state',
                    'seniority', 'leadership_role', 'url', 'total_votes', 'missed_votes', 'missed_votes_pct',
                    'total_present', 'votes_with_party_pct', 'votes_against_party_pct']
with open(memberInfoFileName, 'w', newline='') as memberInfoCSV:
    memberInfoWriter = csv.writer(memberInfoCSV, delimiter=',')
    memberInfoWriter.writerow(memberInfoHeader)
memberInfoCSV.close()

# Hold path of each individual json file
fileLocs = []

# List for used ids
idList = []

# add relevant xml files to fileLocs (-e.json)
for root, dirs, files in os.walk(baseDir):
    for name in files:
        if name.endswith('e.json'):
            fileLocs.append(os.path.join(root, name))

# Reverse file order so that parsing takes place in reverse date order
fileLocs.reverse()

# Parse each file in fileLocs
for file in fileLocs:
    with open(file) as jsonFile:
        jsonData = json.load(jsonFile)

        # relevant data under 'results' list @ [0]
        members = jsonData['results'][0]['members']                     # 'members' is a list with all members
        for member in members:                                          # Parse each member individually
            if member['id'] not in idList:                              # Check to ensure entry does not already exist
                bioguideId = member['id']
                crpId = BioToCrp[bioguideId]
                firstName = member['first_name']
                lastName = member['last_name']
                dateOfBirth = member['date_of_birth']
                gender = member['gender']
                party = member['party']
                state = member['state']
                seniority = member['seniority']
                leadershipRole = member['leadership_role']
                url = member['url']
                totalVotes = member['total_votes']
                missedVotes = member['missed_votes']
                if 'missed_votes_pct' in member:
                    missedVotesPct = member['missed_votes_pct']
                else:
                    missedVotesPct = ''
                totalPresent = member['total_present']
                if 'votes_with_party_pct' in member:
                    votesWithPartyPct = member['votes_with_party_pct']
                else:
                    votesWithPartyPct = ''
                if 'votes_against_party_pct' in member:
                    votesAgainstPartyPct = member['votes_against_party_pct']
                else:
                    votesAgainstPartyPct = ''
                memberInfoRow = [bioguideId, crpId, firstName, lastName, dateOfBirth, gender, party, state, seniority,
                                 leadershipRole, url, totalVotes, missedVotes, missedVotesPct, totalPresent,
                                 votesWithPartyPct, votesAgainstPartyPct]
                with open(memberInfoFileName, 'a', newline='') as memberInfoCSV:
                    memberInfoWriter = csv.writer(memberInfoCSV, delimiter=',')
                    memberInfoWriter.writerow(memberInfoRow)
                memberInfoCSV.close()

                # Add id to list to ensure only one entry per ID
                idList.append(bioguideId)
