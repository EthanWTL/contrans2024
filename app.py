import numpy as np
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from contrans import contrans
import plotly.figure_factory as ff
ct = contrans()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Know Your Representatives in Elected Offices", style={'text-align': 'center'}),
    html.Div([
        dcc.Markdown('To find your representative and Senators, go here: [https://www.congress.gov/members/find-your-member](https://www.congress.gov/members/find-your-member)'),
        dcc.Markdown('Select your representative or Senator here:')
        ], style={'width': '25%', 'float': 'left'}),
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Bio and Contact Info', children=[
                html.Div([
                    html.Img(id = 'bioimage', style={'height':'100%', 'width':'100%'})
                ], style={'width': '28%', 'float': 'left'}),
                html.Div([
                    dcc.Graph(id='biotable')
                ], style={'width': '68%', 'float': 'right'}),
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
# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)