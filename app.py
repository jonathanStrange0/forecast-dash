import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
# app.css.append_css({external_stylesheets:[dbc.themes.CYBORG]})

def build_banner():
    return html.Nav(
        id="banner",
        className="navbar navbar-expand-lg navbar-dark bg-primary",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H3("Forecast Dashboard"),
                    html.H4("Reimplementation of Matt Dancho's shiny code in Dash")
                ])

        ],style={'color': 'white'})

def build_sidebar():
    return html.Div(
        className='four columns',
        style={'color':'black'},
        children=[

            html.Div(
                # className='form-group',
                children=[
                    html.Label('Choose a prediction Model', htmlFor='model'),
                    dbc.Select(
                        id='model',
                    # className='custom-select',
                    options=[{'label':'XGBoost', 'value': 'xgboost'},
                             {'label':'GLMNet', 'value': 'glmnet'}],
                    value='xgboost',
                    )
                ]),

            html.Br(),
            html.Hr(),

            html.Div(
                children=[
                    html.Label('Choose a Product Group'),
                    dbc.Select(
                        className="dcc_control",
                        options=[{'label': 'XGBoost', 'value': 'xgboost'},
                                 {'label': 'GLMNet', 'value': 'glmnet'}],
                        value='xgboost'
                    )
                ]),

            html.Br(),

            html.Div(
                children=[
                    html.Label('Choose a Product Sub Group'),
                    dbc.Select(
                        options=[{'label': 'XGBoost', 'value': 'xgboost'},
                                 {'label': 'GLMNet', 'value': 'glmnet'}],
                        value='xgboost'
                    )
                ]),

            html.Br(),

            html.Div(

                children=[
                    html.Label('Choose Customers'),
                    dbc.Select(
                        # className='form-control',
                        options=[{'label': 'XGBoost', 'value': 'xgboost'},
                                 {'label': 'GLMNet', 'value': 'glmnet'}],
                        value='xgboost'
                    )

                ]),

            html.Br(),
            html.Hr(),

            html.Div(
                children=[
                    html.Label('Choose Time Series Aggregation Period'),
                    # html.Div(className='btn-group btn-group-toggle',
                    #          role='group',
                    #          children=[
                    dbc.ButtonGroup([
                                 dbc.Button('Day',className="btn btn-secondary", id='day', n_clicks=0),
                                 dbc.Button('Week', className="btn btn-secondary", id='week', n_clicks=0 ),
                                 dbc.Button('Month', className="btn btn-secondary", id='month', n_clicks=0),
                                 dbc.Button('Quarter', className="btn btn-secondary", id='quarter', n_clicks=0 ),
                                 dbc.Button('Year', className="btn btn-secondary", id='year', n_clicks=0)
                             ])
                             # ])
                ]),

            html.Br(),

            dbc.FormGroup(
                # className='custom-control custom-switch',
                children=[
                    dbc.Checklist(
                        options=[{"Add Smoother": "Smoother", "value": 1}],
                        # className='custom-control-input',
                        id="smoother",
                        switch=True,
                        value=[]
                    ),
                    html.Label('Add Smoother', className='custom-control-label', htmlFor='smoother'),

                ]
            ),

            html.Br(),

            html.Div(
                children=[
                    html.Label('Choose Time Series Aggregation Period'),
                    dcc.Input('Forecast Horizon', className='form-control-lg')
                ]
            ),

            html.Br(),

            html.Div(
                children=[
                    # html.Label('Choose Time Series Aggregation Period'),
                    html.Button('Calculate Forecast', className='btn btn-success btn-lg')
                ]
            ),

        ]

    )

def build_graph():
    return html.Div(
        className='eight columns',
        style={'color': 'black'},
        children=[
                html.Div(children=[html.H4('Revenue Forecast')], className='ten columns offset by one'),
                  html.Div([
                      dcc.Graph(
                          id='example-graph'
                      )
                  ],
        className='ten columns offset by one'),
        ]
    )

app.layout = html.Div(
    [
    build_banner(),
    html.Div(
        className='twelve columns',
        children=[build_sidebar(),
                  build_graph()]
        )
    ],
    className='twelve columns'
)

@app.callback(dash.dependencies.Output('day', 'active'),
              [dash.dependencies.Input('day', 'n_clicks')])
def update_day_button(n_clicks):
    print('Day')
    if n_clicks % 2 == 0:
        return False
    else:
        return True

@app.callback(dash.dependencies.Output('week', 'active'),
              [dash.dependencies.Input('week', 'n_clicks')])
def update_day_button(n_clicks):
    print('week')
    if n_clicks % 2 == 0:
        return False
    else:
        return True
@app.callback(dash.dependencies.Output('month', 'active'),
              [dash.dependencies.Input('month', 'n_clicks')])
def update_day_button(n_clicks):
    print('Month')
    if n_clicks % 2 == 0:
        return False
    else:
        return True
@app.callback(dash.dependencies.Output('quarter', 'active'),
              [dash.dependencies.Input('quarter', 'n_clicks')])
def update_day_button(n_clicks):
    print('Quarter')
    if n_clicks % 2 == 0:
        return False
    else:
        return True
@app.callback(dash.dependencies.Output('year', 'active'),
              [dash.dependencies.Input('year', 'n_clicks')])
def update_day_button(n_clicks):
    print('Year')
    if n_clicks % 2 == 0:
        return False
    else:
        return True

if __name__ == "__main__":
    app.run_server(debug=True)