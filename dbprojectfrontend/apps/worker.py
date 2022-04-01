from dash import dcc, html, callback, dash_table, State
from dash_extensions.enrich import Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd
from app import app

worker_layout = html.Div([
    dcc.Link('Home Page', href='/'),
    html.H2('Worker Table', style={'textAlign': 'center'}),
    html.Div(id='worker_table'),
    html.H2('Add Worker', style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col(html.Div([
            dbc.Label("Worker SSN"),
            dbc.Input(id="ssn", placeholder='Worker SSN', type="text", value=""),
            dbc.FormFeedback(
                "The length of SSN should be 9",
                type="invalid",
            )
        ]),
            width=2),
        dbc.Col(html.Div([
            dbc.Label("Worker name"),
            dbc.Input(id="name", placeholder='Worker name', type="text", value=""),
        ]),
            width=2),
        dbc.Col(html.Div([
            dbc.Label("Rank"),
            dbc.Input(id="rank", placeholder='Worker rank', type="text", value=""),
            dbc.FormFeedback(
                "Rank should be a positive integer",
                type="invalid",
            )
        ]),
            width=2),
        dbc.Col(html.Div([
            dbc.Label("Employing_state"),
            dbc.Input(id="employing_state", placeholder='Working state abbreviation', type="text", value=""),
            dbc.FormFeedback(
                "State abbreviation should have two characters",
                type="invalid",
            )
        ]),
            width=3),

    ]),
    dbc.Button('Submit', id='add_worker_submit', color='dark', n_clicks=0),
    html.H2("Switch Worker Duties", style={'textAlign': 'center'}),
    dbc.Row(
        [
            dbc.Col(html.Div([
                dbc.Label("Worker1 Name"),
                dbc.Input(id="name1_switch", placeholder='Worker1 name', type="text", value=""),
            ]),
                width=2),
            dbc.Col(html.Div([
                dbc.Label("Worker2 Name"),
                dbc.Input(id="name2_switch", placeholder='Worker2 name', type="text", value=""),
            ]),
                width=2),
        ]
    ),
    dbc.Button('Submit', id='switch_duty_submit', color='dark', n_clicks=0),
    html.Div(id='switch_result'),
    html.H2("Display Top-K Busy Workers", style={'textAlign': 'center'}),
    dbc.Row(
        dbc.Col(html.Div([
            dbc.Label("Enter k"),
            dbc.Input(id="k", placeholder='k', type="text", value=""),
            dbc.FormFeedback(
                "K should be a positive integer",
                type="invalid",
            )
        ]),
            width=1
        )
    ),
    dbc.Button('Submit', id='display_topk', color='dark', n_clicks=0),
    html.Div(id="topk_worker")

])


@app.callback(Output(component_id='worker_table', component_property='children'),
              Input(component_id='add_worker_submit', component_property='n_clicks'),
              State(component_id='ssn', component_property='value'),
              State(component_id='ssn', component_property='invalid'),
              State(component_id='name', component_property='value'),
              State(component_id='rank', component_property='value'),
              State(component_id='rank', component_property='invalid'),
              State(component_id='employing_state', component_property='value'),
              State(component_id='employing_state', component_property='invalid'),
              )
def add_worker(clicks, ssn, ssn_invalid, name, rank, rank_invalid, employing_state,
               employing_state_invalid):
    worker_data = requests.get('https://dbprojectbackend.herokuapp.com/worker/display').json()
    worker_table = pd.DataFrame(worker_data)
    worker_dash_table = dash_table.DataTable(worker_table.to_dict('records'),
                                             [{"name": i, "id": i} for i in
                                              worker_table.columns], page_size=10)
    if clicks == 0:
        return worker_dash_table
    elif clicks > 0:
        if ssn == '' or name == '' or rank == '' or employing_state == '' or ssn_invalid \
                or rank_invalid or employing_state_invalid:
            return html.Div(children=[
                dbc.Alert('Error: input cannot be empty or invalid', color='danger',
                          style={'width': '40%'}),
                worker_dash_table])
        dt = {"ssn": ssn, "name": name, "rank": int(rank), "employing_state": employing_state}

        url = 'https://dbprojectbackend.herokuapp.com/worker/add'
        res = requests.post(url=url, json=dt).json()
        new_data = requests.get('https://dbprojectbackend.herokuapp.com/worker/display').json()
        new_worker_table = pd.DataFrame(new_data)
        new_worker_dash_table = dash_table.DataTable(new_worker_table.to_dict('records'),
                                                     [{"name": i, "id": i} for i in new_worker_table.columns],
                                                     page_size=10)
        if res == 1:
            return html.Div(children=[
                dbc.Alert('Info: insertion is successful!', color='success',
                          style={'width': '30%'}),
                new_worker_dash_table
            ])
        elif res == -1:
            return html.Div(children=[
                dbc.Alert('Error: worker ssn is already in the database!', color='danger',
                          style={'width': '40%'}),
                worker_dash_table,
            ])
        elif res == -2:
            return html.Div(children=[
                dbc.Alert('Error: state name is not in the database!', color='danger',
                          style={'width': '40%'}),
                worker_dash_table,
            ])


@app.callback(Output('switch_result', 'children'),
              Input('switch_duty_submit', 'n_clicks'),
              State('name1_switch', 'value'),
              State('name2_switch', 'value'))
def switch_duty(click, name1, name2):
    if click == 0:
        return None
    if click > 0:
        cond = name1 == '' or name2 == ''
        if cond:
            return dbc.Alert('Error: worker name(names) cannot be empty', color='danger',
                             style={'width': '40%'})
        url = 'https://dbprojectbackend.herokuapp.com/worker/switch'
        dt = {"name1": name1, "name2": name2}
        res = requests.post(url, json=dt).json()
        if res == -1:
            return dbc.Alert('Error: two worker names are the same',
                             style={'width': '40%'})
        elif res == -2:
            return dbc.Alert('Error: the first worker name is not in the database', color='danger',
                             style={'width': '40%'})
        elif res == -3:
            return dbc.Alert('Error: the second worker name is not in the database', color='danger',
                             style={'width': '40%'})
        elif res == -4:
            return dbc.Alert('Error: both worker names are not in the database', color='danger',
                             style={'width': '40%'})
        elif res == -5:
            return dbc.Alert('Error: workers work in different states, canot switch duties!', color='danger',
                             style={'width': '40%'})
        elif res == 1:
            return dbc.Alert('Info: duty switch is successful!', color='success',
                             style={'width': '40%'})


@app.callback(Output(component_id='topk_worker', component_property='children'),
              Input(component_id='display_topk', component_property='n_clicks'),
              State(component_id='k', component_property='value'),
              State(component_id='k', component_property='invalid')
              )
def display_topk(click, k, k_invalid):
    if click == 0:
        return None
    if click > 0:
        if k == '' or k_invalid:
            return dbc.Alert('Error: k cannot be empty or invalid!', color='danger',
                             style={'width': '30%'})
        df = {"k": int(k)}
        url = 'https://dbprojectbackend.herokuapp.com/worker/topk'
        topk_data = requests.post(url=url, json=df).json()
        topk_table = pd.DataFrame(topk_data)
        topk_dash_table = dash_table.DataTable(topk_table.to_dict('records'),
                                               [{"name": i, "id": i} for i in
                                                topk_table.columns], page_size=10)
        return html.Div(children=topk_dash_table, style={'width': '30%'})


@app.callback(Output('ssn', 'invalid'),
              Input('ssn', 'value'))
def validate_ssn(text):
    if text:
        return len(text) != 9
    return False


@app.callback(Output('rank', 'invalid'),
              Input('rank', 'value'))
def validate_rank(text):
    if text:
        if not text.isdigit():
            return True
        return not int(text) > 0
    return False


@app.callback(
    Output("employing_state", "invalid"),
    Input("employing_state", "value")
)
def validate_state_abbreviation(text):
    if text != '':
        return not len(text) == 2
    return False


@app.callback(
    Output("k", "invalid"),
    Input("k", "value")
)
def validate_k(text):
    if text != '':
        if not text.isdigit():
            return True
        return not int(text) > 0
    return False
