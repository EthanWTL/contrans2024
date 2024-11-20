import pandas as pd
import numpy as np
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from contrans import contrans
import os
#import plotly.
ct = contrans()
server, engine = ct.connect_to_postgres(ct.POSTGRES_PASSWORD, host='postgres')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

myquery = '''
SELECT *
FROM members
ORDER BY lastname
'''

members = pd.read_sql_query(myquery,con=engine)

bioguides = members['bioguide']
displayname = members['firstname'] + ' ' + members['lastname'] + '(' + members['partyletter'] + ')'

dropdown_options = [{'label': y,'value': x} for x, y in zip(bioguides, displayname)]

# Populate the layout
app.layout = html.Div([
    html.H1("Know Your Representatives in Elected Offices", style={'text-align': 'center'}),
    html.Div([
        dcc.Markdown('To find your representative and Senators, go here: [https://www.congress.gov/members/find-your-member](https://www.congress.gov/members/find-your-member)'),
        dcc.Markdown('Select your Representative here:'),
        dcc.Dropdown(id='dropdown', options=dropdown_options, value='A000360')
        ], style={'width': '25%', 'float': 'left'}),
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Bio and Contact Info', children=[
                html.Div([
                    html.Img(id='bioimage', style={'height': '100%','width': '100%'}),
                ], style={'width': '28%', 'float': 'left'}),
                html.Div([
                    dcc.Figure(id='biotable')
                ], style={'width': '68%', 'float': 'left'}),
            ]),
            dcc.Tab(label='Ideology and Votes', children=[
                
            ]),
            dcc.Tab(label='Bills', children=[

            ]),
            dcc.Tab(label='News', children=[
                
            ]),
            dcc.Tab(label='Financial Contributors', children=[
                
            ])
        ])
    ], style={'width':'72%', 'float': 'right'}),    
])

@app.callback([Output(component_id='biotable',component_property='src')],
              [Input(component_id='dropdown', component_property='value')])

def biotable(b):
    myquery = f'''
    SELECT directordername AS Name,
        party AS Party,
        state AS State,
        CAST(district AS int) AS District,
        birthyear AS Birthyear,
        addressinformation_officeaddress AS Address,
        CONCAT(addressinformation_city, ', ' , addressinformation_district) AS City,
        addressinformation_zipcode AS Zipcode,
        addressinformation_phonenumber AS Phone
    FROM members
    WHERE bioguideid='{b}'
    '''
    mydf = pd.read_sql_query(myquery, con=engine)
    mydf.columns = [x.capitalize() for x in mydf.columns]
    mydf = mydf.T.reset_index()
    mydf = mydf.rename({'index':'', 0:''}, axis=1)
    return [ff.create_table(mydf)]


def bioimage(b):
    myquery = f'''
    SELECT depiction_imageurl
    FROM members
    WHERE bioguideid='{b}'
    '''
    mydf = pd.read_sql_query(myquery, con=engine)
    return [mydf['depiction_imageurl'][0]]

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
