from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date, datetime

key = 'I60U01EBQ8EXL7J8'

start_date = date.today()
# Choose your output format
ts = TimeSeries(key, output_format='pandas')
ti = TechIndicators(key)

one_year_prior = pd.to_datetime(start_date) + pd.DateOffset(days=-365)
one_year_prior = datetime.strftime(one_year_prior, "%Y-%m-%d")
two_year_prior = pd.to_datetime(start_date) + pd.DateOffset(days=-720)
two_year_prior = datetime.strftime(two_year_prior, "%Y-%m-%d")
three_month_prior = pd.to_datetime(start_date) + pd.DateOffset(days=-90)
three_month_prior = datetime.strftime(three_month_prior, "%Y-%m-%d")

# Get the data, retunrs a tuple
# stock_df is a pandas dataframe, stock_meta_data is a disct
stock_df, stock_meta_data = ts.get_daily(symbol='MDB', outputsize='full')
stock_max = stock_df['4. close'].max()
stock_df['perc_from_max'] = (stock_df['4. close'])/(stock_max)
stock_df['doll_from_max'] = (stock_df['4. close'])-stock_max
stock_df['at_max'] = np.where(stock_df['4. close'] >= stock_max, 1, 0)
stock_df['txn_date'] = stock_df.index

one_year_max = stock_df[stock_df['txn_date'] >= one_year_prior]['4. close'].max()
two_year_max = stock_df[stock_df['txn_date'] >= two_year_prior]['4. close'].max()
three_month_max = stock_df[stock_df['txn_date'] >= three_month_prior]['4. close'].max()
print(stock_df.columns)

stock_df = stock_df.sort_values(['txn_date'], ascending=True)
stock_df['High'] = stock_df['4. close'].cummax()

stock_df['Buy_Ind'] = np.where(stock_df['4. close'] >= stock_df['High'], stock_max, 0)
stock_df['Prior_Day'] = stock_df['txn_date'].shift(30)
stock_df['Prior_Day_High'] = stock_df['High'].shift(30)
stock_df['Prior_Day_Close'] = stock_df['4. close'].shift(30)
stock_df['Prior_month_Buy_Ind'] = stock_df['Buy_Ind'].shift(30)

stock_df['New_Buy_Ind'] = np.where((stock_df['Buy_Ind'] == stock_max) &
                                   (stock_df['Prior_month_Buy_Ind'] != stock_max), stock_max, 0)

print(stock_df[['4. close', 'Buy_Ind', 'High', 'txn_date', 'New_Buy_Ind']].tail(40))

ax = plt.axes
fig = plt.figure()
plt.plot(stock_df['4. close'], label='Close')
plt.plot(stock_df['High'], label='High')
plt.plot(stock_df['New_Buy_Ind'], label='Buy_Ind')
plt.tight_layout()
plt.grid()
plt.legend()
plt.show()

 