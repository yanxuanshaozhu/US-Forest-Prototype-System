from dash import dcc, html, dash_table, State
from app import app, server
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Input, Output
from apps import forest
from apps import worker
from apps import sensor
from apps import coverage
from apps import state
from apps import report

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], style={'background-image': 'url("/assets/forest.jpg")',
          'background-size': '1500px ',
          'background-repeat': 'no-repeat'})

index_layout = html.Div([
    html.H1('Welcome to US Forest System', style={'textAlign': 'center'}),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Forest Page", href='/forest')),
            dbc.NavItem(dbc.NavLink("Coverage Page", href='/coverage')),
            dbc.NavItem(dbc.NavLink("Worker Page", href='/worker')),
            dbc.NavItem(dbc.NavLink("State Page", href='/state')),
            dbc.NavItem(dbc.NavLink("Sensor Page", href='/sensor')),
            dbc.NavItem(dbc.NavLink("Report Page", href="/report")),
        ]
    )
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/forest':
        return forest.forest_layout
    elif pathname == '/worker':
        return worker.worker_layout
    elif pathname == '/sensor':
        return sensor.sensor_layout()
    elif pathname == '/report':
        return report.report_layout()
    elif pathname == '/state':
        return state.state_layout
    elif pathname == '/coverage':
        return coverage.coverage_layout()
    else:
        return index_layout


if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_props_check=False)
