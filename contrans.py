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
    
    def make_header(self, email='wangtianlong1207@gmail.com'):
        useragent = self.get_useragent()
        headers = {'User-Agent': useragent, 'From': email}
        return headers
    
    def get_bioguideIDs(self):
          params={'api_key':self.congresskey}
          headers = self.make_header()
          root = 'https://api.congress.gov/v3'
          endpoint = '/member'
          r = requests.get(root+endpoint, params=params, headers=headers)
          bio_df = pd.json_normalize(r.json(), record_path =['members'])
          bio_df[['name','state','district','bioguideId']]
                
          return bio_df

          