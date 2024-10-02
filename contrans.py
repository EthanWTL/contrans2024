import numpy as np
import pandas as pd
import os
import requests
import json

class contrans:
    def __init__(self):
        self.mypassword=os.getenv('mypassword')
        self.congresskey = os.getenv('congresskey')
        self.newskey = os.getenv('newskey')
    
    def get_votes(self):
            url = 'https://voteview.com/static/data/out/votes/H118_votes.csv'
            votes = pd.read_csv(url)
            return votes
    
    def get_ideology(self):
            url = 'https://voteview.com/static/data/out/members/H118_members.csv'
            members = pd.read_csv(url)
            return members
    
    def get_useragent(self):
          url = 'https://httpbin.org/user-agent'
          r = requests.get(url)
          useragent = json.loads(r.text)['user-agent']
          return useragent
    
    def make_headers(self, email='wangtianlong1207@gmail.com'):
        useragent = self.get_useragent()
        headers = {'User-Agent': useragent, 'From': email}
        return headers
    
    def get_bioguideIDs(self):
                params = {'api_key': self.congresskey,
                          'limit': 1} 
                headers = self.make_headers()
                root = 'https://api.congress.gov/v3'
                endpoint = '/member'
                r = requests.get(root + endpoint,
                                 params=params,
                                 headers=headers)
                totalrecords = r.json()['pagination']['count']
                
                params['limit'] = 250
                j = 0
                bio_df = pd.DataFrame()
                while j < totalrecords:
                        params['offset'] = j
                        r = requests.get(root + endpoint,
                                         params=params,
                                         headers=headers)
                        records = pd.json_normalize(r.json()['members'])
                        bio_df = pd.concat([bio_df, records])
                        j = j + 250

                #bio_df = bio_df[['name', 'state', 'district', 'partyName', 'bioguideId']]
                return bio_df
    
    def get_bioguide(self, name, state=None, district=None):

        members = self.get_bioguideIDs()
        members['name'] = members['name'].str.lower().str.strip()
        name = name.lower().strip()

        tokeep = [name in x for x in members['name']]
        members = members[tokeep]

        if state is not None:
                members = members.query('state == @state')
        if district is not None: 
               members = members.query('district == @district')

        return members.reset_index(drop=True)
    
    def get_sponsoredlegislation(self, bioguideid):

                params = {'api_key': self.congresskey,
                          'limit': 1} 
                headers = self.make_headers()
                root = 'https://api.congress.gov/v3'
                endpoint = f'/member/{bioguideid}/sponsored-legislation'
                r = requests.get(root + endpoint,
                                 params=params,
                                 headers=headers)
                totalrecords = r.json()['pagination']['count']
                
                params['limit'] = 250
                j = 0
                bills_dict = {}
                while j < totalrecords:
                        params['offset'] = j
                        r = requests.get(root + endpoint,
                                         params=params,
                                         headers=headers)
                        records = r.json()['sponsoredLegislation']
                        bills_dict = bills_dict.update(records)
                        j = j + 250

                return bills_dict