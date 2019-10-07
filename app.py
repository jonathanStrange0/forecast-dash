import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

# app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})


def build_banner():
    return html.Nav(
        id="banner",
        className="navbar navbar-expand-lg navbar-dark bg-primary",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H3("Forecast  Dashboard"),
                    html.H4("Reimplementation of Matt Dancho's shiny code in Dash")
                ])

        ],style={'color': 'white'})

def build_sidebar():
    return html.Div(
        className='four columns',
        style={'color':'black'},
        children=[
            html.Div(
                children=[
                    html.Label('Choose a prediction Model'),
                    dcc.Dropdown(
                    # className='btn-group btn-primary',
                    options=[{'label':'XGBoost', 'value': 'xgboost'},
                             {'label':'GLMNet', 'value': 'glmnet'}],
                    value='xgboost'
                    )
                ]),

            html.Br(),
            html.Hr(),

            html.Div(
                children=[
                    html.Label('Choose a Product Group'),
                    dcc.Dropdown(

                        options=[{'label': 'XGBoost', 'value': 'xgboost'},
                                 {'label': 'GLMNet', 'value': 'glmnet'}],
                        value='xgboost'
                    )
                ]),

            html.Br(),

            html.Div(
                children=[
                    html.Label('Choose a Product Sub Group'),
                    dcc.Dropdown(
                        options=[{'label': 'XGBoost', 'value': 'xgboost'},
                                 {'label': 'GLMNet', 'value': 'glmnet'}],
                        value='xgboost'
                    )
                ]),

            html.Br(),

            html.Div(

                children=[
                    html.Label('Choose Customers'),
                    dcc.Dropdown(
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
                    html.Div(className='btn-group',
                             role='group',
                             children=[
                                 html.Button('Day',className="btn btn-primary"),
                                 html.Button('Week', className="btn btn-primary"),
                                 html.Button('Month', className="btn btn-primary"),
                                 html.Button('Quarter', className="btn btn-primary"),
                                 html.Button('Year', className="btn btn-primary"),
                             ])
                    ]
            ),

            html.Br(),

            html.Div(className='custom-control custom-switch',
                children=[
                    dcc.Input(className='custom-control-input', id="smoother"),
                    html.Label('Add Smoother', className='custom-control-label', htmlFor='smoother'),

                ]
            ),

            html.Br(),

            html.Div(
                children=[
                    # html.Label('Choose Time Series Aggregation Period'),
                    html.Button('Calculate Forecast', className='btn btn-primary')
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
                  ], className='ten columns offset by one'),
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


if __name__ == "__main__":
    app.run_server(debug=True)