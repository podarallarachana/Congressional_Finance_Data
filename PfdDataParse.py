# PfdDataParse.py - parses data files to create database tables in the form of .csv files w/ headers for Congressional
#                   candidates' general profile information taken from the pfdMember API at opensecrets.org
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
profileFileName = (pwdPath / '../csv/CandidateProfileTable.csv').resolve()
profileHeader = ['bioguide_id', 'crp_id', 'name', 'data_year', 'net_low', 'net_high', 'positions_held', 'asset_count', 'asset_low', 'asset_high', 'transaction_count', 'tx_low', 'tx_high']
with open(profileFileName, 'w', newline='') as profileCSV:
    profileWriter = csv.writer(profileCSV, delimiter=',')
    profileWriter.writerow(profileHeader)
profileCSV.close()

assetFileName = (pwdPath / '../csv/CandidateAssetTable.csv').resolve()
assetHeader = ['bioguide_id', 'crp_id', 'name', 'data_year', 'asset_name', 'holdings_low', 'holdings_high', 'industry', 'subsidiary_of']
with open(assetFileName, 'w', newline='') as assetCSV:
    assetWriter = csv.writer(assetCSV, delimiter=',')
    assetWriter.writerow(assetHeader)
assetCSV.close()

transactionFileName = (pwdPath / '../csv/CandidateTransactionTable.csv').resolve()
transactionHeader = ['bioguide_id', 'crp_id', 'name', 'data_year', 'asset_name', 'tx_date', 'tx_action', 'value_low', 'value_high']
with open(transactionFileName, 'w', newline='') as transactionCSV:
    transactionWriter = csv.writer(transactionCSV, delimiter=',')
    transactionWriter.writerow(transactionHeader)
transactionCSV.close()

positionsFileName = (pwdPath / '../csv/CandidatePositionsTable.csv').resolve()
positionsHeader = ['bioguide_id', 'crp_id', 'name', 'data_year', 'title', 'organization']
with open(positionsFileName, 'w', newline='') as positionsCSV:
    positionsWriter = csv.writer(positionsCSV, delimiter=',')
    positionsWriter.writerow(positionsHeader)
positionsCSV.close()

# Define current path
curPath = baseDir + 'memPFDprofile'

# Hold path of each individual xml file
fileLocs = []

# add relevant files to fileLocs
for root, dirs, files in os.walk(curPath):
    for name in files:
        if name.endswith('.xml'):
            fileLocs.append(os.path.join(root, name))

# Parse each file in fileLocs
for file in fileLocs:
    tree = ET.parse(file)
    root = tree.getroot()

    # location and data entries; includes general data and information specifically for profile table
    profile = root.find('member_profile')                   # 'member_profile' is one step below root
    crpId = profile.get('member_id')                        # 'member_id' is an attribute of 'profile'
    bioguideId = crToBio[crpId]
    name = profile.get('name')
    dataYear = profile.get('data_year')
    netLow = profile.get('net_low')
    netHigh = profile.get('net_high')
    positionsHeld = profile.get('positions_held_count')
    assetCount = profile.get('asset_count')
    assetLow = profile.get('asset_low')
    assetHigh = profile.get('asset_high')
    transactionCount = profile.get('transaction_count')
    txLow = profile.get('tx_low')
    txHigh = profile.get('tx_high')

    # open profile table and add row
    with open(profileFileName, 'a', newline='') as profileCSV:
        profileWriter = csv.writer(profileCSV, delimiter=',')
        profileRow = [bioguideId, crpId, name, dataYear, netLow, netHigh, positionsHeld, assetCount, assetLow, assetHigh, transactionCount, txLow, txHigh]
        profileWriter.writerow(profileRow)
    profileCSV.close()

    # assets table
    if profile.find('assets') is not None:
        assets = profile.find('assets')
        with open(assetFileName, 'a', newline='') as assetCSV:
            assetWriter = csv.writer(assetCSV, delimiter=',')
            if (len(assets.findall('asset'))) > 1:
                for asset in assets.iter('asset'):
                    assetName = asset.get('name')
                    holdingsLow = asset.get('holdings_low')
                    holdingsHigh = asset.get('holdings_high')
                    industry = asset.get('industry')
                    subsidiaryOf = asset.get('subsidiary_of')
                    assetRow = [bioguideId, crpId, name, dataYear, assetName, holdingsLow, holdingsHigh, industry, subsidiaryOf]
                    assetWriter.writerow(assetRow)
            elif (len(assets.findall('asset'))) == 1:
                asset = assets.find('asset')
                assetName = asset.get('name')
                holdingsLow = asset.get('holdings_low')
                holdingsHigh = asset.get('holdings_high')
                industry = asset.get('industry')
                subsidiaryOf = asset.get('subsidiary_of')
                assetRow = [bioguideId, crpId, name, dataYear, assetName, holdingsLow, holdingsHigh, industry, subsidiaryOf]
                assetWriter.writerow(assetRow)
        assetCSV.close()

    # transactions table
    if profile.find('transactions') is not None:
        transactions = profile.find('transactions')
        with open(transactionFileName, 'a', newline='') as transactionCSV:
            transactionWriter = csv.writer(transactionCSV, delimiter=',')
            if (len(transactions.findall('transaction'))) > 1:
                for transaction in transactions.iter('transaction'):
                    assetName = transaction.get('asset_name')
                    txDate = transaction.get('tx_date')
                    txAction = transaction.get('tx_action')
                    valueLow = transaction.get('value_low')
                    valueHigh = transaction.get('value_high')
                    transactionRow = [bioguideId, crpId, name, dataYear, assetName, txDate, txAction, valueLow, valueHigh]
                    transactionWriter.writerow(transactionRow)
            elif (len(transactions.findall('transaction'))) == 1:
                transaction = transactions.find('transaction')
                assetName = transaction.get('asset_name')
                txDate = transaction.get('tx_date')
                txAction = transaction.get('tx_action')
                valueLow = transaction.get('value_low')
                valueHigh = transaction.get('value_high')
                transactionRow = [bioguideId, crpId, name, dataYear, assetName, txDate, txAction, valueLow, valueHigh]
                transactionWriter.writerow(transactionRow)
        transactionCSV.close()

    # positions table
    if profile.find('positions') is not None:
        positions = profile.find('positions')
        with open(positionsFileName, 'a', newline='') as positionsCSV:
            positionsWriter = csv.writer(positionsCSV, delimiter=',')
            if (len(positions.findall('position'))) > 1:
                for position in positions.iter('position'):
                    title = position.get('title')
                    organization = position.get('organization')
                    positionRow = [bioguideId, crpId, name, dataYear, title, organization]
                    positionsWriter.writerow(positionRow)
            elif (len(positions.findall('position'))) == 1:
                position = positions.find('position')
                title = position.get('title')
                organization = position.get('organization')
                positionRow = [bioguideId, crpId, name, dataYear, title, organization]
                positionsWriter.writerow(positionRow)
        positionsCSV.close()
