#Project Stock viewer Dashboard

#Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import pandas_datareader as web
from datetime import datetime
from iexfinance.stocks import get_historical_data


#Create the application
app = dash.Dash()

#Reading the dataset
df = pd.read_csv('prices.csv', parse_dates=[3])

#creating the options for the Drowpdown menu
options = [{'label': c, 'value':t} for c,t in zip(df['company'].unique(),df['ticker'].unique())]

#Create the layout
app.layout = html.Div([
                html.H1('Stock Ticker Dashboard'),
                
                html.Div([
                    html.H3('Enter a stock symbol:', style={'paddingRight': '30px'}),
                    dcc.Dropdown(id='my-stock-picker',
                    value= ['ITSA4'],
                    options=options,
                    multi=True)
                ], style={'display':'inline-block','verticalAlign':'top', 'width':'30%'}),
                
                html.Div([
                    html.H3('Select a start and end date:'),
                    dcc.DatePickerRange(
                        id='my-date-picker',
                        min_date_allowed=datetime(2020,1,1),
                        max_date_allowed=datetime.today(),
                        start_date=datetime(2020,1,1),
                        end_date=datetime.today()
                        )
                    ], style={'display':'inline-block'}),
                
                html.Div([
                    html.Button(id='submit-button',
                                n_clicks=0,
                                children='Submit',
                                style={'fontSize':24, 'marginLeft':'30px'})
                ], style={'display':'inline-block'}),

                dcc.Graph(id= 'my_graph',
                        figure= {'data':[{'x':[1,2],'y':[3,1]}
                                        ]
                                }
                        )
])

@app.callback(Output('my_graph','figure'),
            [Input('submit-button','n_clicks')],
            [State('my-stock-picker','value'),
            State('my-date-picker','start_date'),
            State('my-date-picker','end_date')])
def update_graph(n_clicks,stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    #df = web.DataReader(stock_ticker,'iex',start, end),
    #df = get_historical_data(stock_ticker, start, end,output_format='pandas',token='test')
    traces = []
    for tic in stock_ticker:
        dff = df[(df['date']>start) & (df['date']<end)]
        dff = dff[dff['ticker']==tic]
        traces.append({'x':dff['date'], 'y':dff['close_price'], 'name':tic})
    fig= {'data':traces,
        'layout':{'title':', '.join(stock_ticker)+' Closing Prices'}}
    return fig


#Run Server
if __name__ == "__main__":
    app.run_server(port=80)

