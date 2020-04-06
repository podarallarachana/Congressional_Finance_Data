import os
import xml.etree.ElementTree as ET
import csv
from pathlib import Path

# URL stub to be used for senate roll call vote conversions to .xml links
SEN_URL_STUB = 'https://www.senate.gov/legislative/LIS/roll_call_votes/vote'

# Change directory based on data files location. As long as files are at or below this
# level and have the proper file name (fdsys_billstatus.xml), they will be parsed.
baseDir = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional Bill Data\\'
pwdPath = Path(__file__)

# CSV filenames and headers
billFileName = (pwdPath / '../csv/BillTable.csv').resolve()
billHeader = ['bill_id', 'type', 'number', 'term', 'origin', 'date_introduced', 'sponsor_id', 'policy_area']
with open(billFileName, 'w', newline='') as billCSV:
    billWriter = csv.writer(billCSV, delimiter=',')
    billWriter.writerow(billHeader)
billCSV.close()

subjectFileName = (pwdPath / '../csv/SubjectTable.csv').resolve()
subjectHeader = ['bill_id', 'subject']
with open(subjectFileName, 'w', newline='') as subjectCSV:
    subjectWriter = csv.writer(subjectCSV, delimiter=',')
    subjectWriter.writerow(subjectHeader)
subjectCSV.close()

cosponsorFileName = (pwdPath / '../csv/CosponsorTable.csv').resolve()
cosponsorHeader = ['bill_id', 'cosponsor', 'is_original_cosponsor', 'start_date', 'withdrawn_date']
with open(cosponsorFileName, 'w', newline='') as cosponsorCSV:
    cosponsorWriter = csv.writer(cosponsorCSV, delimiter=',')
    cosponsorWriter.writerow(cosponsorHeader)
cosponsorCSV.close()

titleFileName = (pwdPath / '../csv/TitleTable.csv').resolve()
titleHeader = ['bill_id', 'title_type', 'parent_title_type', 'chamber', 'title']
with open(titleFileName, 'w', newline='') as titleCSV:
    titleWriter = csv.writer(titleCSV, delimiter=',')
    titleWriter.writerow(titleHeader)
titleCSV.close()

votesFileName = (pwdPath / '../csv/RecordedVotesTable.csv').resolve()
voteHeader = ['bill_id', 'chamber', 'term', 'session', 'action', 'roll_number', 'url']
with open(votesFileName, 'w', newline='') as votesCSV:
    votesWriter = csv.writer(votesCSV, delimiter=',')
    votesWriter.writerow(voteHeader)
votesCSV.close()

billTextFileName = (pwdPath / '../csv/BillTextTable.csv').resolve()
billTextHeader = ['bill_id', 'version_type', 'url']
with open(billTextFileName, 'w', newline='') as billTextCSV:
    billTextWriter = csv.writer(billTextCSV, delimiter=',')
    billTextWriter.writerow(billTextHeader)
billTextCSV.close()

# Hold path of each individual xml file
fileLocs = []

# add relevant xml files to fileLocs (fdsys_billstatus.xml)
for root, dirs, files in os.walk(baseDir):
    for name in files:
        if name.endswith('status.xml'):
            fileLocs.append(os.path.join(root, name))

# Parse each file in fileLocs
for file in fileLocs:
    tree = ET.parse(file)
    root = tree.getroot()

    # xml root = billStatus. All <x>.find are data directly under <x>
    # bill table
    #   location entries
    bill = root.find('bill')                                # 'bill' is one step below root (billStatus->bill)
    sponsors = bill.find('sponsors')                        # billStatus->bill->sponsors
    policy = bill.find('policyArea')                        # billStatus->bill->policyArea
    #   data entries
    billType = bill.find('billType').text                   # billStatus->bill->billType, (e.g., HR, S)
    billNumber = bill.find('billNumber').text               # billStatus->bill->billNumber, int in case it's useful
    term = bill.find('congress').text                       # billStatus->bill->congress, congressional term
    billId = billType + billNumber + '-' + term             # concat 3 strings to get billId
    origin = bill.find('originChamber').text                # billStatus->bill->originChamber, bill origination
    dateIntroduced = bill.find('introducedDate').text       # billStatus->bill->introducedDate
    if sponsors.find('item') is not None:
        sponsor = sponsors.find('item')                     # billStatus->bill->sponsors->item
        sponsorId = sponsor.find('bioguideId').text         # billStatus->bill->sponsors->item->bioguideId
    else:
        sponsorId = ''                                      # No sponsor given
        print('No sponsor found for', billId)
    if policy.find('name') is not None:
        policyArea = policy.find('name').text               # billStatus->bill->policyArea->name
    else:
        policyArea = ''                                     # no policyArea given
        print('No policy area given for', billId)

    # open bills table and add row
    with open(billFileName, 'a', newline='') as billCSV:
        billWriter = csv.writer(billCSV, delimiter=',')
        billRow = [billId, billType, billNumber, term, origin, dateIntroduced, sponsorId, policyArea]
        billWriter.writerow(billRow)
    billCSV.close()

    # subject table
    #   location entry
    #       billStatus->bill->subjects->billSubjects->legislativeSubjects
    subjects = bill.find('subjects').find('billSubjects').find('legislativeSubjects')
    #   data entries
    with open(subjectFileName, 'a', newline='') as subjectCSV:
        subjectWriter = csv.writer(subjectCSV, delimiter=',')
        for item in subjects.iter('item'):
            subject = item.find('name').text
            subjectRow = [billId, subject]
            subjectWriter.writerow(subjectRow)
    subjectCSV.close()

    # cosponsors
    #   location entry
    cosponsors = bill.find('cosponsors')                    # billStatus->bill->cosponsors
    #   data entries
    with open(cosponsorFileName, 'a', newline='') as cosponsorCSV:
        cosponsorWriter = csv.writer(cosponsorCSV, delimiter=',')
        for item in cosponsors.iter('item'):
            cosponsorId = item.find('bioguideId').text
            isOriginalCosponsor = item.find('isOriginalCosponsor').text
            sponsorshipDate = item.find('sponsorshipDate').text
            sponsorshipWithdrawnDate = item.find('sponsorshipWithdrawnDate').text
            sponsorRow = [billId, cosponsorId, isOriginalCosponsor, sponsorshipDate, sponsorshipWithdrawnDate]
            cosponsorWriter.writerow(sponsorRow)
    cosponsorCSV.close()

    # titles
    #   location entry
    titles = bill.find('titles')                            # billStatus->bill->titles
    #   data entries
    title = bill.find('title').text                         # billStatus->bill->title, official bill title
    with open(titleFileName, 'a', newline='') as titleCSV:
        titleWriter = csv.writer(titleCSV, delimiter=',')
        titleFirstRow = [billId, 'Official Title', '', origin, title]
        titleWriter.writerow(titleFirstRow)
        for item in titles.iter('item'):                    # look through titles for all titles
            titleType = item.find('titleType').text
            parentTitleType = item.find('parentTitleType').text
            chamber = item.find('chamberName').text
            itemTitle = item.find('title').text
            titleRow = [billId, titleType, parentTitleType, chamber, itemTitle]
            titleWriter.writerow(titleRow)
    titleCSV.close()

    # votes
    #   location entry
    recordedVotes = bill.find('recordedVotes')              # billStatus->bill->recordedVotes
    #   data entries
    if recordedVotes.find('recordedVote') is not None:
        with open(votesFileName, 'a', newline='') as votesCSV:
            votesWriter = csv.writer(votesCSV, delimiter=',')
            if (len(recordedVotes.findall('recordedVote'))) > 1:
                for vote in recordedVotes.iter('recordedVote'):
                    voteTerm = vote.find('congress').text
                    voteAction = vote.find('fullActionName').text
                    voteRollNumber = vote.find('rollNumber').text
                    voteChamber = vote.find('chamber').text
                    voteSession = vote.find('sessionNumber').text
                    voteUrl = vote.find('url').text
                    # convert Senate vote API links to .xml links
                    if not voteUrl.endswith('.xml'):
                        modUrl = voteUrl.replace('&', ';').replace('=', ';')
                        modList = modUrl.split(';')
                        rollTerm = modList[-5]
                        rollSession = modList[-3]
                        rollCall = modList[-1]
                        voteUrl = SEN_URL_STUB + rollTerm + rollSession + '/vote_' + rollTerm + "_" + rollSession + "_" + rollCall + ".xml"
                    voteRow = [billId, voteChamber, voteTerm, voteSession, voteAction, voteRollNumber, voteUrl]
                    votesWriter.writerow(voteRow)
            elif (len(recordedVotes.findall('recordedVote'))) == 1:
                vote = recordedVotes.find('recordedVote')
                voteTerm = vote.find('congress').text
                voteAction = vote.find('fullActionName').text
                voteRollNumber = vote.find('rollNumber').text
                voteChamber = vote.find('chamber').text
                voteSession = vote.find('sessionNumber').text
                voteUrl = vote.find('url').text
                # convert Senate vote API links to .xml links
                if not voteUrl.endswith('.xml'):
                    modUrl = voteUrl.replace('&', ';').replace('=', ';')
                    modList = modUrl.split(';')
                    rollTerm = modList[-5]
                    rollSession = modList[-3]
                    rollCall = modList[-1]
                    voteUrl = SEN_URL_STUB + rollTerm + rollSession + '/vote_' + rollTerm + "_" + rollSession + "_" + rollCall + ".xml"
                voteRow = [billId, voteChamber, voteTerm, voteSession, voteAction, voteRollNumber, voteUrl]
                votesWriter.writerow(voteRow)
        votesCSV.close()

    # bill text
    #   location & data entries
    #   Skip entries without urls (urls are keys)
    if bill.find('textVersions') is not None:
        textVersions = bill.find('textVersions')            # billStatus->bill->textVersions
        if textVersions.find('item') is not None:
            with open(billTextFileName, 'a', newline='') as billTextCSV:
                billTextWriter = csv.writer(billTextCSV, delimiter=',')
                for textVersion in textVersions.iter('item'):
                    if textVersion.find('type') is not None:
                        versionType = textVersion.find('type').text
                    else:
                        versionType = ''
                    if textVersion.find('formats') is not None:
                        if textVersion.find('formats').find('item') is not None:
                            if textVersion.find('formats').find('item').find('url') is not None:
                                textUrl = textVersion.find('formats').find('item').find('url').text
                                billTextRow = [billId, versionType, textUrl]
                                billTextWriter.writerow(billTextRow)
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
            billTextCSV.close()
