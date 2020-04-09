# ApiDataParse.py - parses data files to create database tables in the form of .csv files w/ headers for Congressional
#                   candidates' industry, sector, and summary information taken from APIs at opensecrets.org
import os
import xml.etree.ElementTree as ET
import csv
import json
from pathlib import Path

# Change directory based on data files location. Additional path information tailored to specific data
baseDir = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\'
pwdPath = Path(__file__)

# Pull in bioguide->crp ID cross reference. Reverse to make crp_id key and bioguide_id only associated value
pathToCR = 'D:\\Users\\daveh\\OneDrive\\Documents\\UF\\CIS4914\\Congressional_Finance_Data\\raw_data\\ppGeneralInfo\\CR.json'
crToBio = {}
with open(pathToCR) as jsonFile:
    crData = json.load(jsonFile)
for key, value in crData.items():
    crToBio[value['crp_Id']] = key

# CSV filenames and headers
candIndFileName = (pwdPath / '../csv/CandidateIndustriesTable.csv').resolve()
candIndHeader = ['bioguide_id', 'crp_id', 'cand_name', 'cycle', 'ind_name', 'indivs', 'pacs', 'totals']
with open(candIndFileName, 'w', newline='') as candIndCSV:
    candIndWriter = csv.writer(candIndCSV, delimiter=',')
    candIndWriter.writerow(candIndHeader)
candIndCSV.close()

candSectFileName = (pwdPath / '../csv/CandidateSectorsTable.csv').resolve()
candSectHeader = ['bioguide_id', 'crp_id', 'cand_name', 'cycle', 'sector_name', 'indivs', 'pacs', 'totals']
with open(candSectFileName, 'w', newline='') as candSectCSV:
    candSectWriter = csv.writer(candSectCSV, delimiter=',')
    candSectWriter.writerow(candSectHeader)
candSectCSV.close()

candSumFileName = (pwdPath / '../csv/CandidateSummaryTable.csv').resolve()
candSumHeader = ['bioguide_id', 'crp_id', 'cand_name', 'cycle', 'state', 'party', 'chamber', 'first_elected', 'next_election', 'total', 'spent', 'cash_on_hand', 'debt']
with open(candSumFileName, 'w', newline='') as candSumCSV:
    candSumWriter = csv.writer(candSumCSV, delimiter=',')
    candSumWriter.writerow(candSumHeader)
candSumCSV.close()

# Election cycles relevant to data (113th, 114th, 115th Congressional terms)
cycles = [2012, 2014, 2016]

# Parse data for each election cycle
for cycle in cycles:

    # Path to files
    candIndPath = baseDir + 'candIndustry\\' + str(cycle)
    candSectPath = baseDir + 'candSector\\' + str(cycle)
    candSumPath = baseDir + 'candSummary\\' + str(cycle)

    # Hold path of each individual xml file
    candIndFileLocs = []
    candSectorFileLocs = []
    candSumFileLocs = []

    ### INDUSTRIES SECTION ###
    # add relevant xml files to fileLocs (*.xml)
    for root, dirs, files in os.walk(candIndPath):
        for name in files:
            if name.endswith('.xml'):
                candIndFileLocs.append(os.path.join(root, name))

    # Parse each file in file list
    for file in candIndFileLocs:
        tree = ET.parse(file)
        root = tree.getroot()                                   # 'response' is root

        industries = root.find('industries')                    # 'industries' is one step below root
        candName = industries.get('cand_name')                  # 'cand_name' is an attribute of 'industries'
        crpId = industries.get('cid')                           # 'cid' is an attribute of 'industries'
        bioguideId = crToBio[crpId]                             # get 'crpId' from cross reference

        # Open csv and append row data
        with open(candIndFileName, 'a', newline='') as candIndCSV:
            candIndWriter = csv.writer(candIndCSV, delimiter=',')
            for industry in industries.iter('industry'):
                industryName = industry.get('industry_name')
                indivs = industry.get('indivs')
                pacs = industry.get('pacs')
                total = industry.get('total')
                candIndRow = [bioguideId, crpId, candName, cycle, industryName, indivs, pacs, total]
                candIndWriter.writerow(candIndRow)
        candIndCSV.close()

    ### SECTORS SECTION ###
    # add relevant xml files to fileLocs (*.xml)
    for root, dirs, files in os.walk(candSectPath):
        for name in files:
            if name.endswith('.xml'):
                candSectorFileLocs.append(os.path.join(root, name))

    # Parse each file in file list
    for file in candSectorFileLocs:
        tree = ET.parse(file)
        root = tree.getroot()                                   # 'response' is root

        sectors = root.find('sectors')                          # 'sectors' is one step below root
        candName = sectors.get('cand_name')                     # 'cand_name' is an attribute of 'sectors'
        crpId = sectors.get('cid')                              # 'cid' is an attribute of 'sectors'
        bioguideId = crToBio[crpId]                             # get 'crpId' from cross reference

        # Open csv and append row data
        with open(candSectFileName, 'a', newline='') as candSectCSV:
            candSectWriter = csv.writer(candSectCSV, delimiter=',')
            for sector in sectors.iter('sector'):
                sectorName = sector.get('sector_name')
                indivs = sector.get('indivs')
                pacs = sector.get('pacs')
                total = sector.get('total')
                candSectRow = [bioguideId, crpId, candName, cycle, sectorName, indivs, pacs, total]
                candSectWriter.writerow(candSectRow)
        candSectCSV.close()

    ### SUMMARY SECTION ###
    # add relevant xml files to fileLocs (*.xml)
    for root, dirs, files in os.walk(candSumPath):
        for name in files:
            if name.endswith('.xml'):
                candSumFileLocs.append(os.path.join(root, name))

    for file in candSumFileLocs:
        tree = ET.parse(file)
        root = tree.getroot()                                   # 'response' is root

        summary = root.find('summary')                          # 'summary' is one step below root
        candName = summary.get('cand_name')                     # 'cand_name' is an attribute of 'summary'
        crpId = summary.get('cid')                              # 'cid' is an attribute of 'summary'
        bioguideId = crToBio[crpId]                             # get 'crpId' from cross reference

        # Open csv and append row data
        with open(candSumFileName, 'a', newline='') as candSumCSV:
            candSumWriter = csv.writer(candSumCSV, delimiter=',')
            state = summary.get('state')
            party = summary.get('party')
            chamber = summary.get('chamber')
            firstElected = summary.get('first_elected')
            nextElection = summary.get('next_election')
            total = summary.get('total')
            spent = summary.get('spent')
            cashOnHand = summary.get('cash_on_hand')
            debt = summary.get('debt')
            candSumRow = [bioguideId, crpId, candName, cycle, state, party, chamber, firstElected, nextElection, total, spent, cashOnHand, debt]
            candSumWriter.writerow(candSumRow)
        candSumCSV.close()
