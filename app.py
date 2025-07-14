import pandas as pd
import json
import yfinance as yf
from plotter import plotter
from predictor import predictor
from dash import Dash, html, dcc, Input, Output, State
from datetime import datetime, date, timedelta
import numpy as np
from df_maker import df_maker
import os
# Load configs
with open('configs.json', 'r') as f:
    configs = json.load(f)

const = configs['const']
coef = configs['coef']
data_path = configs['data_path']
df = pd.read_csv(data_path)
# Add bias columns for old data
df['plus_bias'] = df['Prediction'] * 1.8
df['minus_bias'] = df['Prediction'] * 0.45
df['log_plus_bias'] = np.log2(df['plus_bias'])
df['log_minus_bias'] = np.log2(df['minus_bias'])

date_string = '2024-07-26'
start = datetime.strptime(date_string, '%Y-%m-%d').date()
df_temp = df_maker(const, coef, start)
df = pd.concat([df, df_temp], ignore_index=True)

# Get latest BTC price and date
btc_data = yf.Ticker("BTC-USD")
latest_data = btc_data.history(period="1d")
latest_price = latest_data['Open'].iloc[0]
log2_latest_price = np.log2(latest_price)
latest_date = latest_data.index[0].strftime('%Y-%m-%d')
predict_price, log2_predict_price = predictor(const, coef, latest_date)
buy_price = predict_price * 0.6
sell_price = predict_price * 1.8


# Plot data
fig = plotter(df, 'Date', ['Open', 'Prediction', 'plus_bias', 'minus_bias'], 'BTC/USD')
log_fig = plotter(df, 'Date', ['log2open', 'PredictedLog2Open', 'log_plus_bias', 'log_minus_bias'], 'BTC/USD (Log2)')
tickvals = [1, 10, 100, 1000, 2000, 3000, 4000, 5000]
ticktext = [df['Date'].iloc[i-1] for i in tickvals]
loglog_fig = plotter(df, 'dayth', ['log2open', 'PredictedLog2Open', 'log_plus_bias', 'log_minus_bias'], 'BTC/USD (LogLog)')
loglog_fig.update_layout(xaxis=dict(
        type='log',
        tickvals=tickvals,
        ticktext=ticktext
    ))


app = Dash(__name__,
           meta_tags = [{'name':'viewport',
                       'content': 'width=device-width, initial-scale=0.1, maximum-scale=2,minimun-scale=0.1'}])
server = app.server

# Custom CSS styling
app.layout = html.Div([
    # Header Section
    html.Div([
        html.Div([
            html.H1("₿ Bitcoin Price Predictor for FUN! 🚀🚀🚀🌕", 
                   style={
                       'color': '#F7931A',
                       'fontFamily': 'Segoe UI, Arial, sans-serif',
                       'fontWeight': 'bold',
                       'fontSize': '3rem',
                       'marginBottom': '2rem',
                       'textAlign': 'center'
                   }),
            html.Div([
                html.Span(f"Live Price {latest_date}: ", style={'color': '#F7931A', 'fontSize': '2rem', 'fontWeight': 'bold'}),
                html.Span(f"${'{:,.0f}'.format(latest_price)}", 
                         style={'color': '#FAF9F6', 'fontSize': '2rem', 'fontWeight': 'bold'}),
                html.Span(f" ({'{:.1f}'.format(log2_latest_price)})", 
                         style={'color': '#F7931A', 'fontSize': '2rem', 'fontWeight': 'bold', 'marginLeft': '0.5rem'}),
                # if price is above buy_price, show green "BUY time", else if price is below sell_price, show red "SELL time, else show ""
                html.Br(),
                html.Span(f"Price too low today, BUY time?", style={'color': '#FAF9F6', 'fontSize': '2rem', 'fontWeight': 'bold', 'marginLeft': '0.5rem'}) 
                if latest_price < buy_price else html.Span(f"", style={'color': '#28a745', 'fontSize': '1rem', 'marginLeft': '0.5rem'}),
                html.Br(),
                html.Span(f"Price too high today, SELL time?", style={'color': '#FAF9F6', 'fontSize': '2rem', 'fontWeight': 'bold', 'marginLeft': '0.5rem'}) 
                if latest_price > sell_price else html.Span(f"", style={'color': '#dc3545', 'fontSize': '1rem', 'marginLeft': '0.5rem'}),
                html.Br(),
                html.Span(f"Moderate price today, Hold?", style={'color': '#FAF9F6', 'fontSize': '2rem', 'fontWeight': 'bold', 'marginLeft': '0.5rem'})
                if latest_price > buy_price and latest_price < sell_price else html.Span(f"", style={'color': '#dc3545', 'fontSize': '1rem', 'marginLeft': '0.5rem'}),
                html.Br(),
                # Warning it is not financial advice, just for fun!
                html.Span(f"⚠️ this site is not to provide financial advice, just for fun!", style={'marginBottom': '2rem', 'color': '#F7931A', 'fontSize': '2rem', 'fontWeight': 'bold', 'marginLeft': '0.5rem'})
                ], style={'textAlign': 'center', 'marginBottom': '1rem'})
        ])
    ], style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'padding': '3rem 2rem',
        'marginBottom': '2rem',
        'borderRadius': '0 0 20px 20px',
        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)'
    }),
    
    # Main Content Container
    html.Div([
        # Prediction Input Section
        html.Div([
            html.H3("🔮 Price Prediction", 
                   style={
                       'color': '#343a40',
                       'fontFamily': 'Segoe UI, Arial, sans-serif',
                       'textAlign': 'center',
                       'marginBottom': '1.5rem'
                   }),
            html.Div([
                dcc.Input(
                    id='date-input',
                    type='text',
                    placeholder='Enter date (YYYY-MM-DD)',
                    value='2025-01-01',
                    style={
                        'padding': '12px 20px',
                        'fontSize': '1rem',
                        'borderRadius': '25px',
                        'border': '2px solid #e9ecef',
                        'marginRight': '10px',
                        'width': '200px',
                        'textAlign': 'center',
                        'outline': 'none'
                    }
                ),
                html.Button('Predict', 
                           id='submit-date', 
                           n_clicks=0,
                           style={
                               'padding': '12px 30px',
                               'fontSize': '1rem',
                               'fontWeight': 'bold',
                               'borderRadius': '25px',
                               'border': 'none',
                               'background': 'linear-gradient(45deg, #F7931A, #FFB74D)',
                               'color': 'white',
                               'cursor': 'pointer',
                               'boxShadow': '0 4px 15px rgba(247,147,26,0.3)',
                               'transition': 'all 0.3s ease'
                           })
            ], style={'textAlign': 'center', 'marginBottom': '1rem'}),
            html.Div(id='date-result', style={'textAlign': 'center'})
        ], style={
            'background': 'white',
            'padding': '2rem',
            'borderRadius': '15px',
            'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
            'marginBottom': '2rem'
        }),
        
        # Charts Section
        html.Div([
            # Chart 3: Log-Log Scale
            html.Div([
                html.H4("📈 Log-Log Scale Chart", 
                       style={
                           'color': '#495057',
                           'fontFamily': 'Segoe UI, Arial, sans-serif',
                           'textAlign': 'center',
                           'marginBottom': '1rem'
                       }),
                html.Div(id='hover-info-2', 
                        style={
                            'textAlign': 'center',
                            'fontSize': '1.1rem',
                            'color': '#495057',
                            'marginBottom': '1rem',
                            'minHeight': '30px'
                        }),
                dcc.Graph(id='loglog-price-graph', figure=loglog_fig)
            ], style={
                'background': 'white',
                'padding': '1.5rem',
                'borderRadius': '15px',
                'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
                'marginBottom': '2rem'
            }),
            # Chart 1: Log2 Scale
            html.Div([
                html.H4("📊 Log₂ Scale Chart", 
                       style={
                           'color': '#495057',
                           'fontFamily': 'Segoe UI, Arial, sans-serif',
                           'textAlign': 'center',
                           'marginBottom': '1rem'
                       }),
                html.Div(id='hover-info', 
                        style={
                            'textAlign': 'center',
                            'fontSize': '1.1rem',
                            'color': '#495057',
                            'marginBottom': '1rem',
                            'minHeight': '30px'
                        }),
                dcc.Graph(id='log2-price-graph', figure=log_fig)
            ], style={
                'background': 'white',
                'padding': '1.5rem',
                'borderRadius': '15px',
                'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
                'marginBottom': '2rem'
            }),
            
            # Chart 2: Linear Scale  
            html.Div([
                html.H4("📈 Linear Scale Chart", 
                       style={
                           'color': '#495057',
                           'fontFamily': 'Segoe UI, Arial, sans-serif',
                           'textAlign': 'center',
                           'marginBottom': '1rem'
                       }),
                html.Div(id='hover-info-1', 
                        style={
                            'textAlign': 'center',
                            'fontSize': '1.1rem',
                            'color': '#495057',
                            'marginBottom': '1rem',
                            'minHeight': '30px'
                        }),
                dcc.Graph(id='price-graph', figure=fig)
            ], style={
                'background': 'white',
                'padding': '1.5rem',
                'borderRadius': '15px',
                'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
                'marginBottom': '2rem'
            })
        ])
    ], style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '0 1rem'
    }),
    
    # Footer
    html.Div([
        html.P("Made for fun by DL LIU🤩, not for financial advice! Dash & Plotly | Data from Yahoo Finance", 
               style={
                   'textAlign': 'center',
                   'color': '#6c757d',
                   'fontSize': '0.9rem',
                   'margin': '0'
               })
    ], style={
        'background': '#f8f9fa',
        'padding': '1rem',
        'marginTop': '3rem'
    })
], style={
    'fontFamily': 'Segoe UI, Arial, sans-serif',
    'backgroundColor': '#f8f9fa',
    'minHeight': '100vh',
    'margin': '0',
    'padding': '0'
})

@app.callback(
    Output('date-result', 'children'),
    Input('submit-date', 'n_clicks'),
    State('date-input', 'value')
)
def update_date_result(n_clicks, date_text):
    if n_clicks == 0:
        return html.Div()
    try:
        price_pred, log2_pred = predictor(const, coef, date_text)
    except ValueError:
        return html.Div([
            html.Div("⚠️ Invalid Date Format", 
                    style={
                        'color': '#dc3545',
                        'fontSize': '1.1rem',
                        'fontWeight': 'bold',
                        'marginBottom': '0.5rem'
                    }),
            html.P('Please enter a date in the format YYYY-MM-DD',
                  style={'color': '#6c757d', 'fontSize': '0.9rem'})
        ])
    
    max_date = date(2060, 7, 19)
    min_date = date(2010, 7, 19)
    date_object = datetime.strptime(date_text, '%Y-%m-%d').date()
    if date_object > max_date or date_object < min_date:
        return html.Div([
            html.Div("⚠️ Date Out of Range", 
                    style={
                        'color': '#dc3545',
                        'fontSize': '1.1rem',
                        'fontWeight': 'bold',
                        'marginBottom': '0.5rem'
                    }),
            html.P('Please enter a date between 2010-07-19 and 2060-07-19',
                  style={'color': '#6c757d', 'fontSize': '0.9rem'})
        ])

    return html.Div([
        html.Div([
            html.Div("🎯 Prediction Result", 
                    style={
                        'color': '#28a745',
                        'fontSize': '1.2rem',
                        'fontWeight': 'bold',
                        'marginBottom': '1rem'
                    }),
            html.Div([
                html.Span(f"${'{:,.0f}'.format(price_pred)}", 
                         style={
                             'fontSize': '2.5rem',
                             'fontWeight': 'bold',
                             'color': '#F7931A'
                         }),
                html.Br(),
                html.Span(f"Log₂: {'{:.2f}'.format(log2_pred)}", 
                         style={
                             'fontSize': '1rem',
                             'color': '#6c757d'
                         }),
                html.Br()
            ])
        ], style={
            'background': 'linear-gradient(135deg, #d4edda, #c3e6cb)',
            'padding': '1.5rem',
            'borderRadius': '15px',
            'border': '2px solid #28a745',
            'marginTop': '1rem'
        })
    ])

@app.callback(
    Output('hover-info', 'children'),
    Input('log2-price-graph', 'hoverData'),
)
def display_hover_info(hoverData):
    if hoverData is None:
        return ""
    
    # Extracting information from hoverData
    points = hoverData['points']
    x_value = points[0]['x']
    price_curve_0 = None
    price_curve_1 = None
    price_curve_2 = None
    price_curve_3 = None

    # Loop through points to find prices for curveNumber 0 and 1
    for point in points:
        curve_number = point['curveNumber']
        y_value = point['y']
        if curve_number == 0:
            price_curve_0 = y_value  # Price for curveNumber 0
        elif curve_number == 1:
            price_curve_1 = y_value  # Price for curveNumber 1
        elif curve_number == 2:
            price_curve_2 = y_value  # Price for curveNumber 2
        elif curve_number == 3:
            price_curve_3 = y_value  # Price for curveNumber 3

    # Create styled hover info
    return html.Div([
        html.Span(f"{x_value}: ", style={'color': '#495057', 'fontWeight': 'bold'}),
        html.Span(f"{price_curve_0:.1f}" if price_curve_0 is not None else "", style={'color': '#F7931A', 'fontWeight': 'bold'}),
        html.Span(f" (pred: {price_curve_1:.1f})" if price_curve_1 is not None else "", 
                 style={'color': '#667eea', 'fontWeight': '500'}),
        html.Span(f" (plus bias: {price_curve_2:.1f})" if price_curve_2 is not None else "", 
                 style={'color': '#667eea', 'fontWeight': '500'}),
        html.Span(f" (minus bias: {price_curve_3:.1f})" if price_curve_3 is not None else "", 
                 style={'color': '#667eea', 'fontWeight': '500'})
    ])

@app.callback(
    Output('hover-info-1', 'children'),
    Input('price-graph', 'hoverData'),
)
def display_hover_info_1(hoverData):
    if hoverData is None:
        return ""
    
    # Extracting information from hoverData
    points = hoverData['points']
    x_value = points[0]['x']
    price_curve_0 = None
    price_curve_1 = None
    price_curve_2 = None
    price_curve_3 = None

    # Loop through points to find prices for curveNumber 0 and 1
    for point in points:
        curve_number = point['curveNumber']
        y_value = point['y']
        if curve_number == 0:
            price_curve_0 = y_value  # Price for curveNumber 0
        elif curve_number == 1:
            price_curve_1 = y_value  # Price for curveNumber 1
        elif curve_number == 2:
            price_curve_2 = y_value  # Price for curveNumber 2
        elif curve_number == 3:
            price_curve_3 = y_value  # Price for curveNumber 3

    # Create styled hover info
    return html.Div([
        html.Span(f"{x_value}: ", style={'color': '#495057', 'fontWeight': 'bold'}),
        html.Span(f"${price_curve_0:,.0f}" if price_curve_0 is not None else "", style={'color': '#F7931A', 'fontWeight': 'bold'}),
        html.Span(f" (pred: ${price_curve_1:,.0f})" if price_curve_1 is not None else "", 
                 style={'color': '#667eea', 'fontWeight': '500'}),
        html.Span(f" (plus bias: ${price_curve_2:,.0f})" if price_curve_2 is not None else "", 
                 style={'color': '#667eea', 'fontWeight': '500'}),
        html.Span(f" (minus bias: ${price_curve_3:,.0f})" if price_curve_3 is not None else "", 
                 style={'color': '#667eea', 'fontWeight': '500'})
    ])

@app.callback(
    Output('hover-info-2', 'children'),
    Input('loglog-price-graph', 'hoverData'),
)
def display_hover_info_2(hoverData):
    if hoverData is None:
        return ""
    
    # Extracting information from hoverData
    points = hoverData['points']
    start_date = date(2010, 7, 19)
    x_value = points[0]['x']
    x_value = (start_date + timedelta(days=x_value - 561)).strftime('%Y-%m-%d')
    price_curve_0 = None
    price_curve_1 = None
    price_curve_2 = None
    price_curve_3 = None

    # Loop through points to find prices for curveNumber 0 and 1
    for point in points:
        curve_number = point['curveNumber']
        y_value = point['y']
        if curve_number == 0:
            price_curve_0 = y_value  # Price for curveNumber 0
        elif curve_number == 1:
            price_curve_1 = y_value  # Price for curveNumber 1
        elif curve_number == 2:
            price_curve_2 = y_value  # Price for curveNumber 2
        elif curve_number == 3:
            price_curve_3 = y_value  # Price for curveNumber 3

    # Create styled hover info
    return html.Div([
        html.Span(f"{x_value}: ", style={'color': '#495057', 'fontWeight': 'bold'}),
        html.Span(f"{price_curve_0:.1f}" if price_curve_0 is not None else "", style={'color': '#F7931A', 'fontWeight': 'bold'}),
        html.Span(f" (pred: {price_curve_1:.1f})" if price_curve_1 is not None else "", 
                 style={'color': '#667eea', 'fontWeight': '500'}),
        html.Span(f" (plus bias: {price_curve_2:.1f})" if price_curve_2 is not None else "", 
                 style={'color': '#667eea', 'fontWeight': '500'}),
        html.Span(f" (minus bias: {price_curve_3:.1f})" if price_curve_3 is not None else "", 
                 style={'color': '#667eea', 'fontWeight': '500'})
    ])


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    # Run the app
    app.run_server(host='0.0.0.0', port=port, debug=True)