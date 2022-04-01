from dash import dcc, html, dash_table, State
from dash_extensions.enrich import Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd
from app import app

state_layout = html.Div(children=[
    dcc.Link('Home Page', href='/'),
    html.H2('State Table', style={'textAlign': 'center'}),
    html.Div(id='state_result'),
    html.H2("Add State", style={'textAlign': 'center'}),
    html.Div(children=[
        dbc.Row([
            dbc.Col(
                html.Div(
                    [
                        dbc.Label("Name"),
                        dbc.Input(id="name", placeholder='State name', type="text", value=""),
                    ]
                )
            ),
            dbc.Col(
                html.Div(
                    [
                        dbc.Label("Abbreviation"),
                        dbc.Input(id="abbreviation", placeholder='State abbreviation', type="text", value=""),
                        dbc.FormFeedback(
                            "State abbreviation should have two characters",
                            type="invalid",
                        ),
                    ]
                )
            ),
            dbc.Col(
                html.Div(
                    [
                        dbc.Label("Area"),
                        dbc.Input(id="area", placeholder='Sate area', type="text", value=""),
                        dbc.FormFeedback(
                            "Area should be a positive number",
                            type="invalid",
                        ),
                    ]
                )
            ),
            dbc.Col(
                html.Div(
                    [
                        dbc.Label("Population"),
                        dbc.Input(id="population", placeholder='State population', type="text", value=""),
                        dbc.FormFeedback(
                            "Population should be a positive integer",
                            type="invalid",
                        ),
                    ]
                )
            )]
        ),
        dbc.Button('Submit', id='add_state_submit', color='dark', n_clicks=0)
    ])
])


@app.callback(Output(component_id='state_result', component_property='children'),
              Input('add_state_submit', 'n_clicks'),
              State('name', 'value'),
              State('abbreviation', 'value'),
              State('abbreviation', 'invalid'),
              State('area', 'value'),
              State('area', 'invalid'),
              State('population', 'value'),
              State('population', 'invalid')
              )
def add(click, name, abbreviation, abbreviation_invalid, area, area_invalid, population, population_invalid):
    state_data = requests.get('https://dbprojectbackend.herokuapp.com/state/display').json()
    state_table = pd.DataFrame(state_data)
    state_dash_table = dash_table.DataTable(state_table.to_dict('records'),
                                            [{"name": i, "id": i} for i in
                                             state_table.columns], page_size=10)
    if click == 0:
        return state_dash_table
    elif click > 0:
        if name == '' or abbreviation == '' or area == '' or population == '' or abbreviation_invalid \
                or area_invalid or population_invalid:
            return html.Div(children=[
                dbc.Alert('Error: input cannot be empty or invalid!', color='danger',
                          style={'width': '30%'}),
                state_dash_table
            ])
        dt = {"name": name, "abbreviation": abbreviation, "area": float(area), "population": int(population)}
        url = 'https://dbprojectbackend.herokuapp.com/state/add'
        res = requests.post(url=url, json=dt).json()
        if res == 1:
            new_data = requests.get('https://dbprojectbackend.herokuapp.com/state/display').json()
            new_state_table = pd.DataFrame(new_data)
            new_state_dash_table = dash_table.DataTable(new_state_table.to_dict('records'),
                                                        [{"name": i, "id": i} for i in
                                                         new_state_table.columns], page_size=10)
            return html.Div(children=[
                dbc.Alert('Info: insertion is successful!', color='success',
                          style={'width': '40%'}),
                new_state_dash_table
            ])
        elif res == -1:
            return html.Div(children=[
                dbc.Alert('Error: the state name is already in the database!', color='danger',
                          style={'width': '40%'}),
                state_dash_table
            ])
        elif res == -2:
            return html.Div(children=[
                dbc.Alert('Error: the state abbreviation is already in the database!', color='danger',
                          style={'width': '40%'}),
                state_dash_table
            ])


@app.callback(
    Output("abbreviation", "invalid"),
    Input("abbreviation", "value")
)
def validate_abbreviation(text):
    if text != '':
        return not len(text) == 2
    return False


def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


@app.callback(
    Output("area", "invalid"),
    Input("area", "value")
)
def validate_area(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) > 0
    return False


@app.callback(
    Output("population", "invalid"),
    Input("population", "value")
)
def validate_population(text):
    if text != '':
        if not text.isdigit():
            return True
        return not int(text) > 0
    return False
