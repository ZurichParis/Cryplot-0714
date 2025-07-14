import pandas as pd
import yfinance as yf
import numpy as np
from datetime import date, datetime, timedelta

def df_maker(const, coef, start, ticker='BTC-USD'):
    # Fetch historical data from Yahoo Finance
    data = yf.Ticker(ticker).history(start=start)
    df = pd.DataFrame(data)
    df.reset_index(inplace=True)  # Reset index to make Date a column
    df['Date'] = df['Date'].dt.date  # Convert Date to date type (removing time)
    df['Date'] = df['Date'].astype(str)
    df = df[['Date', 'Open']]
    
    # Generate future dates up to 1 year from today
    today = datetime.now().date()
    future_end_date = today + timedelta(days=365)
    
    # Get the last date from Yahoo Finance data
    last_yahoo_date = pd.to_datetime(df['Date'].iloc[-1]).date()
    
    # Create future dates from the day after last Yahoo date to 1 year from today
    if last_yahoo_date < future_end_date:
        future_dates = pd.date_range(
            start=last_yahoo_date + timedelta(days=1),
            end=future_end_date,
            freq='D'
        ).date
        
        # Create future dataframe with predictions only (no Open prices)
        future_df = pd.DataFrame({
            'Date': [str(d) for d in future_dates],
            'Open': [np.nan] * len(future_dates)  # non open price for future days
        })
        
        # Combine historical and future data
        df = pd.concat([df, future_df], ignore_index=True)
    
    # Calculate predictions for all dates (historical and future)
    df['dayth'] = (pd.to_datetime(df['Date']) - pd.to_datetime(date(2010, 7, 19))).dt.days + 561
    df['log2open'] = np.log2(df['Open'])  # Will be NaN for future dates
    df['log2dayth'] = np.log2(df['dayth'])
    df['PredictedLog2Open'] = df['log2dayth']*coef + const
    df['Prediction'] = 2 ** df['PredictedLog2Open']
    
    # Add bias columns
    df['plus_bias'] = df['Prediction'] * 1.8
    df['minus_bias'] = df['Prediction'] * 0.45
    df['log_plus_bias'] = np.log2(df['plus_bias'])
    df['log_minus_bias'] = np.log2(df['minus_bias'])
    
    return df