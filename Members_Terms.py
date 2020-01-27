import requests
import json
import pandas as pd
import csv
from xml.etree import ElementTree

#initialize variables
Column_names = ['member_id', 'first_name', 'middle_name', 'last_name',
                'gender', 'in_office', 'seniority', 'state', 'cycle',
                'chamber', 'next_election', 'total_votes', 'missed_votes',
                'votes_against_party_pct', 'missed_votes_pct', 'votes_with_party_pct',
                'party', 'crp_id', 'debt', 'total', 'spent', 'cash_on_hand']

member_id = ''
first_name = ''
middle_name = ''
last_name = ''
gender = ''
in_office = ''
seniority = ''
state = ''
cycle = ''
chamber = ''
next_election = ''
total_votes = ''
missed_votes = ''
votes_against_party_pct = ''
missed_votes_pct = ''
votes_with_party_pct = ''
party = ''
crp_id = ''
debt = ''
total = ''
spent = ''
cash_on_hand = ''

# 102-116 for House, 80-116 for Senate (ProPublica Data)
house_low = 102
house_high = 116
senate_low = 80
senate_high = 116

PROPUBLICA_API_KEY = ''
OPEN_SECRETS_API_KEY = ''

# makes requests to ProPublica API for all congress member information and loads info into variables
def load_data(term, chamber):
            s = requests.Session()
            s.headers.update({'x-test': 'true'})
            responose = s.get('https://api.propublica.org/congress/v1/' + str(term) + '/'
            + chamber + '/members.json', headers={'X-API-Key': PROPUBLICA_API_KEY})
            json_data = json.loads(responose.text)['results']

            cycle = json_data[0]['congress']
            chamber = json_data[0]['chamber']

            for member in json_data[0]['members']:
                  member_id = member['id']
                  first_name = member['first_name']
                  middle_name = member['middle_name']
                  last_name = member['last_name']
                  gender = member['gender']
                  in_office = member['in_office']
                  seniority = member['seniority']
                  state = member['state']
                  party = member['party']
                  crp_id = member['crp_id']

                  # years (Open Secrets API) -> congress cycles (ProPublica API)
                  # 2020 -> 116
                  # 2018 -> 115
                  # 2016 -> 114
                  # 2014 -> 113
                  # 2012 -> 112

                  #if crp_id is not null, get basic campaign finance info
                  if(crp_id is not None and term >= 112 and term <= 116):
                      if(term == 112):
                          response = requests.get('https://www.opensecrets.org/api/'
                                                  '?method=candSummary&cid=' + crp_id + '&cycle=' + '2012' +
                                                  '&apikey=0da28a05ff606b574ec9e5df9c741618')
                      elif(term == 113):
                          response = requests.get('https://www.opensecrets.org/api/'
                                                  '?method=candSummary&cid=' + crp_id + '&cycle=' + '2014' +
                                                  '&apikey=0da28a05ff606b574ec9e5df9c741618')
                      elif (term == 114):
                          response = requests.get('https://www.opensecrets.org/api/'
                                                  '?method=candSummary&cid=' + crp_id + '&cycle=' + '2016' +
                                                  '&apikey=0da28a05ff606b574ec9e5df9c741618')
                      elif (term == 115):
                          response = requests.get('https://www.opensecrets.org/api/'
                                                  '?method=candSummary&cid=' + crp_id + '&cycle=' + '2018' +
                                                  '&apikey=0da28a05ff606b574ec9e5df9c741618')
                      elif (term == 116):
                          response = requests.get('https://www.opensecrets.org/api/'
                                                  '?method=candSummary&cid=' + crp_id + '&cycle=' + '2020' +
                                                  '&apikey=0da28a05ff606b574ec9e5df9c741618')
                      print(str(crp_id) + '             '  + str(term))
                      if "Resource not found" not in response.content.decode("utf-8"):
                          tree = ElementTree.fromstring(response.content)
                          for x in tree:
                            debt = x.get('debt')
                            total = x.get('total')
                            spent = x.get('spent')
                            cash_on_hand = x.get('cash_on_hand')
                      else:
                          debt = ''
                          total = ''
                          spent = ''
                          cash_on_hand = ''
                  else:
                      debt = ''
                      total = ''
                      spent = ''
                      cash_on_hand = ''

                  if 'next_election' in member:
                        next_election = member['next_election']
                  else:
                        next_election = ''

                  total_votes = member['total_votes']
                  missed_votes = member['missed_votes']

                  if 'votes_against_party_pct' in member:
                        votes_against_party_pct = member['votes_against_party_pct']
                  else:
                        votes_against_party_pct = ''

                  if 'missed_votes_pct' in member:
                        missed_votes_pct = member['missed_votes_pct']
                  else:
                        missed_votes_pct = ''

                  if 'votes_with_party_pct' in member:
                        votes_with_party_pct = member['votes_with_party_pct']
                  else:
                        votes_with_party_pct = ''


                  wr.writerow([member_id, first_name, middle_name, last_name,
                            gender, in_office, seniority, state, cycle,
                            chamber, next_election, total_votes, missed_votes,
                            votes_against_party_pct, missed_votes_pct, votes_with_party_pct,
                            party, crp_id, debt, total, spent, cash_on_hand])


#save data into csv
with open('../raw_data/ProPublica_Member_data.csv', 'w', newline='', encoding='utf-8') as myfile:
      wr = csv.writer(myfile, delimiter=',')
      wr.writerow(Column_names)
      for x in range(senate_low, senate_high + 1):
            load_data(x, 'senate')
      for x in range(house_low, house_high + 1):
            load_data(x, 'house')

#remove congress_members who do not have crp_ids (no use to this project since their financial info is not available)
df = pd.read_csv('../raw_data/member_terms_data.csv')
df = df[pd.notnull(df['crp_id'])]
df.to_csv('../raw_data/member_terms_data.csv')

