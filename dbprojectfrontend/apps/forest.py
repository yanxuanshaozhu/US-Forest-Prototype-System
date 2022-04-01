from dash import dcc, html, dash_table, State
from dash_extensions.enrich import Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd
from app import app

forest_layout = html.Div([
    dcc.Link('Home Page', href='/'),
    html.H2('Forest Table', style={'textAlign': 'center'}),
    html.Div(id='forest_table'),
    html.H2('Add Forest', style={'textAlign': 'center'}),
    html.Div(children=[
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dbc.Label("Forest Name"),
                            dbc.Input(id="name", placeholder='Forest name', type="text", value=""),
                        ]
                    ),
                    width=2
                ),
                dbc.Col(
                    html.Div(
                        [
                            dbc.Label("Area"),
                            dbc.Input(id="area", placeholder='Forest area', type="text", value=""),
                            dbc.FormFeedback(
                                "Area should be a positive number",
                                type="invalid",
                            )
                        ]
                    ),
                    width=2
                ),
                dbc.Col(
                    html.Div(
                        [
                            dbc.Label("Acid_level"),
                            dbc.Input(id="acid_level", placeholder='Forest acid_level', type="text", value=""),
                            dbc.FormFeedback(
                                "Acid_level should be a positive number",
                                type="invalid",
                            )
                        ]
                    ),
                    width=2
                ),
                dbc.Col(
                    html.Div(
                        [
                            dbc.Label("State"),
                            dbc.Input(id="state", placeholder='Covered state name', type="text", value=""),
                        ]),
                    width=2
                )
            ]
        ),
        dbc.Row([
            dbc.Col(
                html.Div(
                    [
                        dbc.Label("Mbr_xmin"),
                        dbc.Input(id="mbr_xmin", placeholder='Forest mbr_xmin', type="text", value=""),
                        dbc.FormFeedback(
                            "Mbr_xmin should be a positive number",
                            type="invalid",
                        )
                    ]
                ),
                width=2
            ),
            dbc.Col(
                html.Div(
                    [
                        dbc.Label("Mbr_xmax"),
                        dbc.Input(id="mbr_xmax", placeholder='Forest mbr_xmax', type="text", value=""),
                        dbc.FormFeedback(
                            "Mbr_xmax should be a positive number",
                            type="invalid",
                        )
                    ]
                ),
                width=2
            ),
            dbc.Col(
                html.Div(
                    [
                        dbc.Label("Mbr_ymin"),
                        dbc.Input(id="mbr_ymin", placeholder='Forest mbr_ymin', type="text", value=""),
                        dbc.FormFeedback(
                            "Mbr_ymin should be a positive number",
                            type="invalid",
                        )
                    ]
                ),
                width=2
            ),
            dbc.Col(
                html.Div(
                    [
                        dbc.Label("Mbr_ymax"),
                        dbc.Input(id="mbr_ymax", placeholder='Forest mbr_ymax', type="text", value=""),
                        dbc.FormFeedback(
                            "Mbr_ymax should be a positive number",
                            type="invalid",
                        )
                    ]
                ),
                width=2
            ),
        ]),
        dbc.Button('Submit', id='add_forest_submit', n_clicks=0, color='dark')
    ]),
    html.H2("Update Forest Coverage", style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col(
            html.Div([
                dbc.Label("Forest Name"),
                dbc.Input(id="name_update", placeholder='New forest name', type="text", value="")
            ]),
            width=2

        ),
        dbc.Col(
            html.Div([
                dbc.Label("Area"),
                dbc.Input(id="area_update", placeholder='New forest area', type="text", value=""),
                dbc.FormFeedback(
                    "Area should be a positive number",
                    type="invalid",
                )
            ]),
            width=2
        ),
        dbc.Col(
            html.Div(
                [
                    dbc.Label("State"),
                    dbc.Input(id="state_update", placeholder='Covered state abbreviation', type="text", value=""),
                    dbc.FormFeedback(
                        "State abbreviation should have two characters",
                        type="invalid",
                    ),
                ]
            ),
            width=3
        ),
    ]),
    dbc.Button('Submit', id='update_forest_submit', color='dark', n_clicks=0)

])


@app.callback(Output(component_id='forest_table', component_property='children'),
              Input(component_id='add_forest_submit', component_property='n_clicks'),
              State(component_id='name', component_property='value'),
              State(component_id='area', component_property='value'),
              State(component_id='area', component_property='invalid'),
              State(component_id='acid_level', component_property='value'),
              State(component_id='acid_level', component_property='invalid'),
              State(component_id='mbr_xmin', component_property='value'),
              State(component_id='mbr_xmin', component_property='invalid'),
              State(component_id='mbr_xmax', component_property='value'),
              State(component_id='mbr_xmax', component_property='invalid'),
              State(component_id='mbr_ymin', component_property='value'),
              State(component_id='mbr_ymin', component_property='invalid'),
              State(component_id='mbr_ymax', component_property='value'),
              State(component_id='mbr_ymax', component_property='invalid'),
              State(component_id='state', component_property='value')
              )
def add_forest(clicks, name, area, area_invalid, acid_level, acid_level_invalid,
               mbr_xmin, mbr_xmin_invalid, mbr_xmax, mbr_xmax_invalid,
               mbr_ymin, mbr_ymin_invalid, mbr_ymax, mbr_ymax_invalid, state):
    forest_data = requests.get('https://dbprojectbackend.herokuapp.com/forest/display').json()
    forest_table = pd.DataFrame(forest_data)
    forest_dash_table = dash_table.DataTable(forest_table.to_dict('records'),
                                             [{"name": i, "id": i} for i in
                                              forest_table.columns], page_size=10)
    if clicks == 0:
        return forest_dash_table
    elif clicks > 0:
        if name == '' or area == '' or acid_level == '' or mbr_xmin == '' or mbr_xmax == '' \
                or mbr_ymin == '' or mbr_ymax == '' or area_invalid or acid_level_invalid \
                or mbr_xmin_invalid or mbr_xmax_invalid or mbr_ymin_invalid or mbr_ymax_invalid:
            return html.Div(children=[
                dbc.Alert("Input cannot be empty or invalid", color='danger', style={'width': '30%'}),
                forest_dash_table])
        dt = {"name": name, "area": float(area), "acid_level": float(acid_level),
              "mbr_xmin": float(mbr_xmin), "mbr_xmax": float(mbr_xmax),
              "mbr_ymin": float(mbr_ymin), "mbr_ymax": float(mbr_ymax),
              "state": state}

        url = 'https://dbprojectbackend.herokuapp.com/forest/add'
        res = requests.post(url=url, json=dt).json()
        new_data = requests.get('https://dbprojectbackend.herokuapp.com/forest/display').json()
        new_forest_table = pd.DataFrame(new_data)
        new_forest_dash_table = dash_table.DataTable(new_forest_table.to_dict('records'),
                                                     [{"name": i, "id": i} for i in new_forest_table.columns],
                                                     page_size=10)
        if res == 1:
            return html.Div(children=[
                dbc.Alert('Info: insertion is successful!', color='success', style={'width': '30%'}),
                new_forest_dash_table
            ])
        elif res == -1:
            return html.Div(children=[
                dbc.Alert('Error: forest name is already contained in the database!', color='danger',
                          style={'width': '40%'}),
                forest_dash_table,
            ])
        elif res == -2:
            return html.Div(children=[
                dbc.Alert('Error: state name is not contained in the database!', color='danger',
                          style={'width': '40%'}),
                forest_dash_table,
            ])


@app.callback(Output('forest_table', 'children'),
              Input('update_forest_submit', 'n_clicks'),
              State('name_update', 'value'),
              State('area_update', 'value'),
              State('area_update', 'invalid'),
              State('state_update', 'value'),
              State('state_update', 'invalid')
              )
def update(click, name, area, area_invalid, state, state_invalid):
    cond = name == '' or area == '' or state == '' or area_invalid or state_invalid
    forest_data = requests.get('https://dbprojectbackend.herokuapp.com/forest/display').json()
    forest_table = pd.DataFrame(forest_data)
    forest_dash_table = dash_table.DataTable(forest_table.to_dict('records'),
                                             [{"name": i, "id": i} for i in
                                              forest_table.columns], page_size=10)
    if click == 0:
        return html.Div(children=[
            forest_dash_table
        ])
    if click > 0:
        if cond:
            return html.Div(children=[
                dbc.Alert('Error: input cannot be empty or invalid!', color='danger', style={'width': '40%'}),
                forest_dash_table
            ])
    dt = {"name": name, "area": float(area), "state": state.upper()}
    url = 'https://dbprojectbackend.herokuapp.com/forest/update'
    res = requests.post(url=url, json=dt).json()
    new_data = requests.get('https://dbprojectbackend.herokuapp.com/forest/display').json()
    new_table = pd.DataFrame(new_data)
    new_dash_table = dash_table.DataTable(new_table.to_dict('records'),
                                          [{"name": i, "id": i} for i in
                                           new_table.columns], page_size=10)
    if res == 1:
        return html.Div(children=[
            dbc.Alert('Info: update is successful!', color='success', style={'width': '30%'}),
            new_dash_table
        ])
    elif res == -1:
        return html.Div(children=[
            dbc.Alert('Error: forest name is not contained in the database!', color='danger',
                      style={'width': '40%'}),
            forest_dash_table
        ])
    elif res == -2:
        return html.Div(children=[
            dbc.Alert('Error: state abbreviation is not contained in the database!', color='danger',
                      style={'width': '40%'}),
            forest_dash_table
        ])


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
def check_validity(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) > 0
    return False


@app.callback(
    Output("acid_level", "invalid"),
    Input("acid_level", "value")
)
def check_validity(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) > 0
    return False


@app.callback(
    Output("mbr_xmin", "invalid"),
    Input("mbr_xmin", "value")
)
def check_validity(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) > 0
    return False


@app.callback(
    Output("mbr_xmax", "invalid"),
    Input("mbr_xmax", "value")
)
def check_validity(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) > 0
    return False


@app.callback(
    Output("mbr_ymin", "invalid"),
    Input("mbr_ymin", "value")
)
def check_validity(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) > 0
    return False


@app.callback(
    Output("mbr_ymax", "invalid"),
    Input("mbr_ymax", "value")
)
def check_validity(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) > 0
    return False


@app.callback(
    Output("area_update", "invalid"),
    Input("area_update", "value")
)
def check_validity(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) > 0
    return False


@app.callback(
    Output("state_update", "invalid"),
    Input("state_update", "value")
)
def check_validity(text):
    if text != '':
        return not len(text) == 2
    return False
