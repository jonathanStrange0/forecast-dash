import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Output, Input
from functions.collect_bike_data import collect_bike_data
from functions.aggregate_time_series import aggregate_time_series
from functions.predict_n_future_sales import predict_n_future_sales
import pandas as pd
import numpy as np

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
df = collect_bike_data("assets/bikes_database.sqlite")
# print(df.head())


### Helper functions ###
def filter_table(product_group_values, prod_sub_group_values,customer_values):
    print(product_group_values, '\n', prod_sub_group_values, '\n', customer_values)
    product_group_filter = ''.join([x + '|' for x in product_group_values])[:-1]
    prod_subgroup_filter = ''.join([x + '|' for x in prod_sub_group_values])[:-1]
    customer_filter = ''.join([x + '|' for x in customer_values])[:-1]

    print('Filters \n', product_group_filter, '\n', prod_subgroup_filter, '\n', customer_filter)

    product_group_mask = df['category.1'].str.contains(product_group_filter, regex=True)
    prod_subgroup_mask = df['category.2'].str.contains(prod_subgroup_filter, regex=True)
    customer_mask = df['bikeshop.name'].str.contains(customer_filter, regex=True)

    print('Masks \n', product_group_mask.value_counts(), '\n', prod_subgroup_mask.value_counts(), '\n',
          customer_mask.value_counts())

    filtered_bikes_df = df[product_group_mask & prod_subgroup_mask & customer_mask]

    return filtered_bikes_df

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
                             {'label':'Elastic Net', 'value': 'elastic_net'}],
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
                        options=[{'label': name, 'value': name} for name in \
                                                        np.sort(df['category.1'].unique().tolist())],
                        multi=True,
                        value=[name for name in np.sort(df['category.1'].unique().tolist())],
                    )
                ]),

            html.Br(),

            html.Div(
                children=[
                    html.Label('Choose a Product Sub Group'),
                    dcc.Dropdown(
                        id='product-subgroup',
                        options=[{'label': name, 'value': name} for name in \
                                                        np.sort(df['category.2'].unique().tolist())],
                        value=[name for name in np.sort(df['category.2'].unique().tolist())],
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
                        options=[{'label': name, 'value': name} for name in \
                                 np.sort(df['bikeshop.name'].unique().tolist())],
                        value=[name for name in np.sort(df['bikeshop.name'].unique().tolist())],
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
                    dcc.Dropdown(
                                className="select",
                                id='date-agg',
                                options=[
                                    {'label':'Day','value':'Day'},
                                    {'label': 'Week', 'value':'Week'},
                                    {'label': 'Month', 'value':'Month'},
                                    {'label': 'Quarter', 'value':'Quarter'},
                                    {'label': 'Year', 'value':'Year'}
                             ],
                                value='Week'
                    )
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
                              value = 12,
                              className='form-control-lg')
                ]
            ),

            html.Br(),

            html.Div(
                children=[
                    # html.Label('Choose Time Series Aggregation Period'),
                    html.Button('Calculate Forecast',
                                id='forecast',
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
                          id='forecast-graph'
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


@app.callback(Output('forecast-graph', 'figure'),
              [Input('forecast', 'n_clicks'),
                Input('model', 'value'),
               Input('product-group', 'value'),
               Input('product-subgroup', 'value'),
               Input('customers', 'value'),
                Input('date-agg', 'value'),
               Input('horizon', 'value')
               ])
def update_forecast_button(n_clicks,
                           model,
                           product_group_values,
                           prod_sub_group_values,
                           customer_values,
                           date_agg_value,
                           horizon):

    filtered_bikes_df = filter_table(product_group_values, prod_sub_group_values,customer_values)

    sales_df, agg_period = aggregate_time_series(filtered_bikes_df, date_agg_value)

    print(sales_df.head())

    history = go.Scatter(x=list(sales_df.index),
                         y=list(sales_df.price_ext),
                         name='Sales History',
                         line=dict(color='#2C3E4D'))

    prediction, dates = predict_n_future_sales(sales_df, n_future=int(horizon), period=agg_period, model=model)

    print(prediction, dates)
    print()

    future = go.Scatter(x=list(dates),
                         y=list(prediction),
                         name='Sales Forecast',
                         line=dict(color='#cc1606'))

    graph_layout = dict(title='Sales Forecast Chart')

    fig = dict(data=[history, future],
               layout=graph_layout)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)


