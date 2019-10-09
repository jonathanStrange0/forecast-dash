import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from functions.collect_bike_data import collect_bike_data
import pandas as pd
import numpy as np

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
df = collect_bike_data("assets/bikes_database.sqlite")
print(df.head())

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
                    dcc.Dropdown(
                        id='product-group',
                        className="dcc_control",
                        options=[{'label': name, 'value': name.lower()} for name in \
                                                        np.sort(df['category.1'].unique().tolist())],
                        multi=True,
                        value=[name.lower() for name in np.sort(df['category.1'].unique().tolist())],
                    )
                ]),

            html.Br(),

            html.Div(
                children=[
                    html.Label('Choose a Product Sub Group'),
                    dcc.Dropdown(
                        id='product-subgroup',
                        options=[{'label': name, 'value': name.lower()} for name in \
                                                        np.sort(df['category.2'].unique().tolist())],
                        value=[name.lower() for name in np.sort(df['category.2'].unique().tolist())],
                        multi=True
                    )
                ]),

            html.Br(),

            html.Div(

                children=[
                    html.Label('Choose Customers'),
                    dcc.Dropdown(
                        id='customers',
                        className ="select",
                        options=[{'label': name, 'value': name.lower()} for name in \
                                 np.sort(df['bikeshop.name'].unique().tolist())],
                        value=[name.lower() for name in np.sort(df['bikeshop.name'].unique().tolist())],
                        multi=True
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
                    dbc.ButtonGroup(
                                className="btn-group btn-group-radio",
                                id='date-agg',
                                children=[
                                 dbc.Button('Day',className="btn btn-primary", id='day', n_clicks=0, color='primary'),
                                 dbc.Button('Week', className="btn btn-primary", id='week', n_clicks=0, color='primary'),
                                 dbc.Button('Month', className="btn btn-primary", id='month', n_clicks=0, color='primary'),
                                 dbc.Button('Quarter', className="btn btn-primary", id='quarter', n_clicks=0, color='primary'),
                                 dbc.Button('Year', className="btn btn-primary", id='year', n_clicks=0, color='primary')
                             ])
                             # ])
                ]),

            html.Br(),

            dbc.FormGroup(
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
                    dcc.Input(id='horizon',
                              className='form-control-lg')
                ]
            ),

            html.Br(),

            html.Div(
                children=[
                    # html.Label('Choose Time Series Aggregation Period'),
                    html.Button('Calculate Forecast',
                                id='foreceast',
                                className='btn btn-success btn-lg'),
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
                          id='graph'
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

#
# @app.callback(Output('btnGroup', 'children'),
#               [Input('day', 'n_clicks')])
# def update_day_button(n_clicks):
#
#     if n_clicks % 2 == 0 or n_clicks == 0:
#         print('Day', n_clicks)
#         return dict(id="day",
#                 active=False)
#     else:
#         return True


@app.callback(Output('week', 'active'),
              [Input('week', 'n_clicks')])
def update_day_button(n_clicks):

    if n_clicks % 2 == 0 or n_clicks == 0:

        return False
    else:
        print('week')
        return True


@app.callback(Output('month', 'active'),
              [Input('month', 'n_clicks')])
def update_day_button(n_clicks):

    if n_clicks % 2 == 0 or n_clicks == 0:

        return False
    else:
        print('Month')
        return True


@app.callback(Output('quarter', 'active'),
              [Input('quarter', 'n_clicks')])
def update_day_button(n_clicks):

    if n_clicks % 2 == 0 or n_clicks == 0:

        return False
    else:
        print('Quarter')
        return True


@app.callback(Output('year', 'active'),
              [Input('year', 'n_clicks')])
def update_day_button(n_clicks):

    if n_clicks % 2 == 0 or n_clicks == 0:

        return False
    else:
        print('Year')
        return True


@app.callback(Output('forecast-graph', 'figure'),
              [Input('forecast', 'n_clicks'),
               Input('product-group', 'value'),
               Input('product-subgroup', 'value'),
                Input('customers', 'value')
               ])
def update_forecast_button(n_clicks,
                           product_group_values,
                           prod_sub_group_values,
                           customer_values):
    product_group_filter = ''.join([x+'|' for x in product_group_values])
    prod_subgroup_filter = ''.join([x + '|' for x in prod_sub_group_values])
    customer_filter = ''.join([x + '|' for x in customer_values])
    filtered_bikes_df = df[(df['category.1'].str.contains(product_group_filter)) &
                           (df['category.2'].str.contains(prod_subgroup_filter)) &
                           (df['bikeshop.name'].str.contains(customer_filter))]

    return filtered_bikes_df


if __name__ == "__main__":
    app.run_server(debug=True)