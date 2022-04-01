from dash import dcc, html, callback, dash_table, State
import requests
import pandas as pd


def report_layout():
    report_data = requests.get('https://dbprojectbackend.herokuapp.com/report/display').json()
    report_table = pd.DataFrame(report_data)
    report_dash_table = dash_table.DataTable(report_table.to_dict('records'),
                                             [{"name": i, "id": i} for i in
                                              report_table.columns], page_size=10)
    return html.Div(children=[
        dcc.Link('Home Page', href='/'),
        html.H2('Report Table', style={'textAlign': 'center'}),
        html.Div(id='forest_table', children=report_dash_table)
    ])
