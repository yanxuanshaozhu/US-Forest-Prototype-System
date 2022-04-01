from dash import dcc, html, dash_table, State
from dash_extensions.enrich import Output, Input
import dash_bootstrap_components as dbc
import requests
import pandas as pd
from app import app


def sensor_layout():
    sensor_data = requests.get('https://dbprojectbackend.herokuapp.com/sensor/display').json()
    sensor_table = pd.DataFrame(sensor_data)
    sensor_dash_table = dash_table.DataTable(sensor_table.to_dict('records'),
                                             [{"name": i, "id": i} for i in
                                              sensor_table.columns], page_size=8)
    return html.Div([
        dcc.Link('Home Page', href='/'),
        html.H2('Sensor Table', style={'textAlign': 'center'}),
        html.Div(id='sensor_table_div', children=sensor_dash_table),
        html.H2('Add Sensor', style={'textAlign': 'center'}),
        dbc.Row([
            dbc.Col(html.Div([
                dbc.Label("Sensor_id"),
                dbc.Input(id="sensor_id", placeholder='Sensor_id', type="text", value=""),
                dbc.FormFeedback(
                    "Sensor_id should be a positive integer",
                    type="invalid",
                )
            ]),
                width=2),
            dbc.Col(html.Div([
                dbc.Label("X"),
                dbc.Input(id="x", placeholder='X-coordinate', type="text", value=""),
                dbc.FormFeedback(
                    "X should be a non-negative real number",
                    type="invalid",
                )
            ]),
                width=2),
            dbc.Col(html.Div([
                dbc.Label("Y"),
                dbc.Input(id="y", placeholder='Y-coordinate', type="text", value=""),
                dbc.FormFeedback(
                    "Y should be a non-negative real number",
                    type="invalid",
                )
            ]),
                width=2),
            dbc.Col(html.Div([
                dbc.Label("Last_charged"),
                dbc.Input(id="last_charged", placeholder='Last charged datetime', type="datetime-local", value=""),
            ]),
                width=2),
            dbc.Col(html.Div([
                dbc.Label("Maintainer"),
                dbc.Input(id="maintainer", placeholder='Maintainer SSN', type="text", value=""),
                dbc.FormFeedback(
                    "Worker SSN should have length 9",
                    type="invalid",
                )
            ]),
                width=2),
        ]),
        dbc.Row([
            dbc.Col(html.Div([
                dbc.Label("Last_read"),
                dbc.Input(id="last_read", placeholder='Last read datetime', type="datetime-local", value=""),
            ]),
                width=2),
            dbc.Col(html.Div([
                dbc.Label("Energy"),
                dbc.Input(id="energy", placeholder='Energy level', type="text", value=""),
                dbc.FormFeedback(
                    "Energy should be a non-negative real number",
                    type="invalid",
                )
            ]),
                width=2),

        ]),
        dbc.Button('Submit', id='add_sensor_submit', color='dark', n_clicks=0),
        html.H2("Update Sensor Status", style={'textAlign': 'center'}),
        dbc.Row([
            dbc.Col(html.Div([
                dbc.Label("X"),
                dbc.Input(id="x_update", placeholder='X-coordinate', type="text", value=""),
                dbc.FormFeedback(
                    "X should be a non-negative real number",
                    type="invalid",
                )
            ]),
                width=2),
            dbc.Col(html.Div([
                dbc.Label("Y"),
                dbc.Input(id="y_update", placeholder='Y-coordinate', type="text", value=""),
                dbc.FormFeedback(
                    "Y should be a non-negative real number",
                    type="invalid",
                )
            ]),
                width=2),
            dbc.Col(html.Div([
                dbc.Label("Energy"),
                dbc.Input(id="energy_update", placeholder='Energy level', type="text", value=""),
                dbc.FormFeedback(
                    "Energy should be a non-negative real number",
                    type="invalid",
                )
            ]),
                width=2),
            dbc.Col(html.Div([
                dbc.Label("Last_charged"),
                dbc.Input(id="last_charged_update", placeholder='Last read datetime', type="datetime-local", value=""),
            ]),
                width=2),
            dbc.Col(html.Div([
                dbc.Label("Temperature"),
                dbc.Input(id="temperature_update", placeholder='Temperature', type="text", value=""),
                dbc.FormFeedback(
                    "Temperature should be a real number",
                    type="invalid",
                )
            ]),
                width=2),
        ]),
        dbc.Button('Submit', id='update_sensor_submit', color='dark', n_clicks=0),
        html.H2("Most Active Sensors", style={'textAlign': 'center'}),
        html.Div(id='most_active'),
        dbc.Row([
            dbc.Col(html.Div([
                dbc.Label("K"),
                dbc.Input(id="k_active", placeholder='Top K active sensor', type="text", value=""),
                dbc.FormFeedback(
                    "K should be a positive integer",
                    type="invalid",
                )
            ]),
                width=3),
        ]),
        dbc.Button('Display', id='display_active_sensor', color='dark', n_clicks=0)
    ])


@app.callback(Output('sensor_table_div', 'children'),
              Input(component_id='add_sensor_submit', component_property='n_clicks'),
              State(component_id='sensor_id', component_property='value'),
              State(component_id='sensor_id', component_property='invalid'),
              State(component_id='x', component_property='value'),
              State(component_id='x', component_property='invalid'),
              State(component_id='y', component_property='value'),
              State(component_id='y', component_property='invalid'),
              State(component_id='last_charged', component_property='value'),
              State(component_id='maintainer', component_property='value'),
              State(component_id='maintainer', component_property='invalid'),
              State(component_id='last_read', component_property='value'),
              State(component_id='energy', component_property='value'),
              State(component_id='energy', component_property='invalid'),
              )
def add(click, sensor_id, sensor_id_invalid, x, x_invalid, y, y_invalid, last_charged, maintainer,
        maintainer_invalid, last_read, energy, energy_invalid):
    sensor_data = requests.get('https://dbprojectbackend.herokuapp.com/sensor/display').json()
    sensor_table = pd.DataFrame(sensor_data)
    sensor_dash_table = dash_table.DataTable(sensor_table.to_dict('records'),
                                             [{"name": i, "id": i} for i in
                                              sensor_table.columns], page_size=8)
    if click == 0:
        return sensor_dash_table
    if click > 0:
        print(len(maintainer))
        cond = sensor_id == '' or x == '' or y == '' or last_charged == '' \
               or last_read == '' or energy == '' \
               or sensor_id_invalid or x_invalid or y_invalid or maintainer_invalid or energy_invalid
        if cond:
            return html.Div(children=[
                dbc.Alert('Error: input cannot be empty or invalid', color='danger',
                          style={'width': '30%'}),
                sensor_dash_table
            ])

        dt = {"sensor_id": int(sensor_id), "x": float(x), "y": float(y),
              "last_charged": last_charged.replace("T", " ") + ":00", "maintainer": maintainer,
              "last_read": last_read.replace("T", " ") + ":00", "energy": float(energy)}
        url = 'https://dbprojectbackend.herokuapp.com/sensor/add'
        res = requests.post(url=url, json=dt).json()
        new_data = requests.get('https://dbprojectbackend.herokuapp.com/sensor/display').json()
        new_sensor_table = pd.DataFrame(new_data)
        new_sensor_dash_table = dash_table.DataTable(new_sensor_table.to_dict('records'),
                                                     [{"name": i, "id": i} for i in new_sensor_table.columns],
                                                     page_size=8)
        if res == 1:
            return html.Div(children=[
                dbc.Alert('Info: insertion is successful!', color='success',
                          style={'width': '30%'}),
                new_sensor_dash_table
            ])
        elif res == -1:
            return html.Div(children=[
                dbc.Alert('Error: sensor_id is already in the database', color='danger',
                          style={'width': '40%'}),
                sensor_dash_table,
            ])
        elif res == -2:
            return html.Div(children=[
                dbc.Alert('Error: sensor location is already in the database', color='danger',
                          style={'width': '40%'}),
                sensor_dash_table,
            ])
        elif res == -3:
            return html.Div(children=[
                dbc.Alert('Error: sensor maintainer ssn is not in the database', color='danger',
                          style={'width': '40%'}),
                sensor_dash_table
            ])


@app.callback(Output(component_id='sensor_table_div', component_property='children'),
              Input(component_id='update_sensor_submit', component_property='n_clicks'),
              State(component_id='x_update', component_property='value'),
              State(component_id='x_update', component_property='invalid'),
              State(component_id='y_update', component_property='value'),
              State(component_id='y_update', component_property='invalid'),
              State(component_id='energy_update', component_property='value'),
              State(component_id='energy_update', component_property='invalid'),
              State(component_id='last_charged_update', component_property='value'),
              State(component_id='temperature_update', component_property='value'),
              State(component_id='temperature_update', component_property='invalid'),
              )
def update(click, x_update, x_update_invalid, y_update, y_update_invalid, energy_update,
           energy_update_invalid, last_charged_update, temperature_update, temperature_update_invalid):
    sensor_data = requests.get('https://dbprojectbackend.herokuapp.com/sensor/display').json()
    sensor_table = pd.DataFrame(sensor_data)
    sensor_dash_table = dash_table.DataTable(sensor_table.to_dict('records'),
                                             [{"name": i, "id": i} for i in
                                              sensor_table.columns], page_size=8)
    if click == 0:
        return sensor_dash_table
    if click > 0:
        cond = x_update == '' or y_update == '' or energy_update == '' or last_charged_update == '' \
               or temperature_update == '' or x_update_invalid or y_update_invalid or energy_update_invalid \
               or temperature_update_invalid
        if cond:
            return html.Div(children=[
                dbc.Alert('Error: input cannot be empty or invalid', color='danger',
                          style={'width': '30%'}),
                sensor_dash_table
            ])
        dt = {"x": float(x_update), "y": float(y_update), "energy": float(energy_update),
              "last_charged": last_charged_update.replace("T", " ") + ":00", "temperature": float(temperature_update)}
        url = 'https://dbprojectbackend.herokuapp.com/sensor/update'
        res = requests.post(url=url, json=dt).json()
        new_data = requests.get('https://dbprojectbackend.herokuapp.com/sensor/display').json()
        new_sensor_table = pd.DataFrame(new_data)
        new_sensor_dash_table = dash_table.DataTable(new_sensor_table.to_dict('records'),
                                                     [{"name": i, "id": i} for i in new_sensor_table.columns],
                                                     page_size=8)
        if res == 2:
            return html.Div(children=[
                dbc.Alert('Info: update is successful! High temperature alert!', color='danger',
                          style={'width': '40%'}),
                new_sensor_dash_table
            ])
        elif res == 1:
            return html.Div(children=[
                dbc.Alert('Info: update is successful!', color='success', style={
                    'width': '30%'}),
                new_sensor_dash_table
            ])
        elif res == -1:
            return html.Div(children=[
                dbc.Alert('Error: there is no sensor at the location in the database!', color='danger',
                          style={'width': '40%'}),
                sensor_dash_table
            ])


@app.callback(Output('most_active', 'children'),
              Input('display_active_sensor', 'n_clicks'),
              State('k_active', 'value'),
              State('k_active', 'invalid'))
def display_active(click, k, k_invalid):
    if click > 0:
        if k == '' or k_invalid:
            return dbc.Alert('Error: input cannot be empty or invalid!', color='danger',
                             style={'width': '30%'})
        dt = {"k": int(k)}
        active_data = requests.post('https://dbprojectbackend.herokuapp.com/sensor/ranking', json=dt).json()
        active_table = pd.DataFrame(active_data)
        active_dash_table = dash_table.DataTable(active_table.to_dict('records'),
                                                 [{"name": i, "id": i} for i in
                                                  active_table.columns], page_size=8)
        return html.Div(children=[active_dash_table], style={'width': '30%'})


@app.callback(
    Output("sensor_id", "invalid"),
    Input("sensor_id", "value")
)
def validate_sensor_id(text):
    if text != '':
        if not text.isdigit():
            return True
        return not int(text) > 0
    return False


def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


@app.callback(
    Output("x", "invalid"),
    Input("x", "value")
)
def validate_x(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) >= 0
    return False


@app.callback(
    Output("y", "invalid"),
    Input("y", "value")
)
def validate_y(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) >= 0
    return False


@app.callback(
    Output("maintainer", "invalid"),
    Input("maintainer", "value")
)
def validate_maintainer(text):
    if text != '':
        return not len(text) == 9
    return False


@app.callback(
    Output("energy", "invalid"),
    Input("energy", "value")
)
def validate_energy(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) >= 0
    return False


@app.callback(
    Output('x_update', "invalid"),
    Input('x_update', "value")
)
def validate_x_update(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) >= 0
    return False


@app.callback(
    Output('y_update', "invalid"),
    Input('y_update', "value")
)
def validate_y_update(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) >= 0
    return False


@app.callback(
    Output('energy_update', "invalid"),
    Input('energy_update', "value")
)
def validate_energy_update(text):
    if text != '':
        if not is_float(text):
            return True
        return not float(text) >= 0
    return False


@app.callback(
    Output('temperature_update', "invalid"),
    Input('temperature_update', "value")
)
def validate_temperature_update(text):
    if text != '':
        return not is_float(text)
    return False


@app.callback(
    Output('k_active', "invalid"),
    Input('k_active', "value")
)
def validate_k_active(text):
    if text != '':
        if not text.isdigit():
            return True
        return not int(text) > 0
    return False
