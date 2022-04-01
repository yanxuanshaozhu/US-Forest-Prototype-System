from dash import dcc, html, dash_table
import requests
import pandas as pd


def coverage_layout():
    coverage_data = requests.get('https://dbprojectbackend.herokuapp.com/coverage/display').json()
    coverage_table = pd.DataFrame(coverage_data)
    coverage_dash_table = dash_table.DataTable(coverage_table.to_dict('records'),
                                               [{"name": i, "id": i} for i in
                                                coverage_table.columns], page_size=10)
    return html.Div(children=[
        dcc.Link('Home Page', href='/'),
        html.H2('Coverage Table', style={'textAlign': 'center'}),
        html.Div(id='coverage_table', children=coverage_dash_table),

    ])
