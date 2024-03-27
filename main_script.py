import datetime
import matplotlib.pyplot as plt
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import seaborn as sns
sns.set(style="whitegrid")

#fetch daily ohcl data
def get_daily_spot_data(symbol,start_date, end_date):
    # URL for Binance's spot market data
    url = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': '1d',
        'limit': 1000
    }

    data = []
    current_date = start_date

    while current_date < end_date:
        params['startTime'] = int(current_date.timestamp() * 1000)
        params['endTime'] = int(min(current_date + timedelta(days=365), end_date).timestamp() * 1000)
        response = requests.get(url, params=params)
        data += response.json()
        current_date += timedelta(days=365)

    df = pd.DataFrame(data, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
    df['Open Time'] = pd.to_datetime(df['Open Time'],unit='ms')
    df.index = df['Open Time']

    # Convert the relevant columns to float
    float_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in float_columns:
        df[col] = df[col].astype(float)
    return df[float_columns]

#compute daily volitility
def getDailyVol(close,span0=100):
    # daily vol reindexed to close
    df0=close.index.searchsorted(close.index-pd.Timedelta(days=1))
    df0=df0[df0>0]
    df0=(pd.Series(close.index[df0-1],
                   index=close.index[close.shape[0]-df0.shape[0]:]))
    try:
        df0=close.loc[df0.index]/close.loc[df0.values].values-1 # daily rets
    except Exception as e:
        print(f'error: {e}\nplease confirm no duplicate indices')
    print(df0)
    df0=df0.ewm(span=span0).std().rename('dailyVol')
    return df0

#fetch daily marketcap
def get_market_cap(coin_id, start_date, end_date):
    # CoinGecko API endpoint for historical market data, using coin_id for flexibility
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range"

    # Formatting start and end dates as timestamps
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    params = {
        'vs_currency': 'usd',
        'from': start_timestamp,
        'to': end_timestamp
    }

    # Fetching the data from CoinGecko
    response = requests.get(url, params=params)
    data = response.json()

    # Extracting market cap data
    market_caps = data['market_caps']

    # Creating a DataFrame
    df = pd.DataFrame(market_caps, columns=['Date', 'Market Cap'])
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.set_index('Date', inplace=True)

    return df



def fetch_pool_data_to_dataframe(start_date,end_date,pool_address):
    # Convert the start date to a Unix timestamp
    start_timestamp = int(start_date.timestamp())
    # Current date to a Unix timestamp
    end_timestamp = int(end_date.timestamp())

    # GraphQL query
    query = """
    query ($poolId: ID!, $dateGt: Int!, $dateLt: Int!) {
      poolDayDatas(first: 1000, orderBy: date, orderDirection: asc, where: {
        pool: $poolId,
        date_gt: $dateGt,
        date_lt: $dateLt
      }) {
        date
        liquidity
        sqrtPrice
        token0Price
        token1Price
        volumeToken0
        volumeToken1
      }
    }
    """

    # The Graph API URL for Uniswap
    url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'

    # Make the POST request with the updated query
    response = requests.post(url, json={'query': query, 'variables': {'poolId': pool_address, 'dateGt': start_timestamp,
                                                                      'dateLt': end_timestamp}})

    # Check the response status and process the data
    if response.status_code == 200:
        data = response.json()['data']['poolDayDatas']

        # Prepare the data list
        formatted_data = []
        for entry in data:
            # Convert the timestamp to a readable date format
            date_formatted = datetime.utcfromtimestamp(int(entry['date'])).strftime('%Y-%m-%d')

            # Convert liquidity to a more understandable unit (assuming it's in wei for demonstration)
            liquidity_formatted = float(entry['liquidity']) / 1e18

            # Calculate the actual price ratio (assuming the sqrtPrice is the square root of the price for demonstration)
            price = (float(entry['sqrtPrice']) ** 2) / 1e18

            formatted_data.append({
                'Date': date_formatted,
                'Liquidity (ETH)': liquidity_formatted,
                'Price': price,
                'Token0Price': entry['token0Price'],
                'Token1Price': entry['token1Price'],
                'VolumeToken0': entry['volumeToken0'],
                'VolumeToken1': entry['volumeToken1']
            })

        # Convert to DataFrame
        df = pd.DataFrame(formatted_data)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        return df
    else:
        print("Failed to fetch data:", response.status_code)
        return pd.DataFrame()  # Return an empty DataFrame on failure

def picture_out(df,col,color,name):
    plt.figure(figsize=(14, 6))
    sns.lineplot(x=df.index, y=df[col], color=color, label=col)
    plt.title(col+' Over Time')
    plt.xlabel('Date')
    plt.ylabel(col)
    plt.legend()
    plt.show()
    plt.savefig(col+name)
    return 'ALL DONE'

def corr_matrix(df_scaled):
    # Set up the matplotlib figure
    plt.figure(figsize=(10, 8))
    corr = df_scaled.corr()
    # Generate a heatmap
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm',
                xticklabels=corr.columns, yticklabels=corr.columns,
                cbar_kws={"shrink": .75})

    # Adjust layout for better readability
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=45)
    plt.title('Correlation Matrix Heatmap')
    # Show plot
    plt.show()
    return 'Correlation Matrix Done'

def main_output(start_date,end_date,symbol,coin_id,pool_address,span):
    # Fetching the data from binance
    df = get_daily_spot_data(symbol, start_date, end_date)
    # print(df.dtypes)  # This will show the data types of the columns

    market_cap_df = get_market_cap(coin_id, start_date, end_date)
    # print(btc_market_cap_df.head())  # Print the first few rows of the DataFrame

    # Calculate the daily volatility for the 'Close' column
    df['Daily_Volatility'] = getDailyVol(df['Close'], span0=30)
    # Calculate the daily return rate for the 'Close' column
    df['Daily_Return'] = df['Close'].pct_change()
    df = pd.concat([df, market_cap_df], axis=1)

    pool_df = fetch_pool_data_to_dataframe(start_date, end_date, pool_address)
    df = pd.concat([df, pool_df], axis=1)
    # print(df.head())

    column_selected = ['Volume', 'Daily_Volatility', 'Market Cap', 'Liquidity (ETH)']
    df_selected = df[column_selected].loc[start_date + timedelta(days=span):, ]
    print(df_selected.describe())

    df_scaled = (df_selected - df_selected.min()) / (df_selected.max() - df_selected.min()) * (5 - 1) + 1
    print(df_scaled.describe())
    df_scaled['Combine_Feature'] = df_scaled['Volume'] * df_scaled['Market Cap'] * df_scaled['Liquidity (ETH)'] / \
                                   df_scaled['Daily_Volatility']
    return df_selected,df_scaled


if __name__ == "__main__":
    for i in range(3):
        try:
            # Setting the date range
            start_date = datetime(2023, 4, 1)
            end_date = datetime.now()
            symbol = 'ETHUSDT'
            coin_id = 'ethereum'
            # ETH-USDC pool address in Uniswap
            pool_address = "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8"
            span = 30
            df_selected, df_scaled = main_output(start_date, end_date, symbol,coin_id, pool_address, span)
            print(df_selected)
            print(df_scaled)
            print(df_selected.corr())
            print(df_scaled.corr())
            corr_matrix(df_scaled)
            time.sleep(5)
            break
        except Exception as e:
            continue






