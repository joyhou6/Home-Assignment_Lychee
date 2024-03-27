Project: Crypto Asset Quality Evalution

This project is designed to fetch, analyze, and visualize cryptocurrency market data including trading data from Binance, market capitalization from CoinGecko, and liquidity pool information from Uniswap. It features the ability to analyze data over a specified date range for various cryptocurrencies and liquidity pools. The analysis includes daily open-high-low-close (OHLC) values, daily market cap, daily volatility, and liquidity pool data, providing insights into market trends and dynamics.

Dependencies:

This project requires Python 3.x and the following Python libraries:
pandas
matplotlib
seaborn
requests

Installation:

Before running the project, ensure you have Python 3.x installed on your system. Then, install the required dependencies by running the following command in your terminal:
pip install pandas matplotlib seaborn requests 

Project Files:

main_script.py: The main Python script containing all the functions for fetching, processing, and visualizing the data.
requirements.txt: A file listing all the necessary Python packages.

How to Use:

Set Up Your Environment:
Ensure Python 3.x and all dependencies listed in requirements.txt are installed.
Place the main_script.py in your project directory.

Configuration:

Open main_script.py in a text editor or IDE.
Set the start_date(only support dates in the past year due to pubic API limit) and end_date variables to define the period for your analysis.
Configure the symbol variable for the cryptocurrency pair you are interested in (e.g., 'ETHUSDT').
Set the coin_id to the specific cryptocurrency you want to analyze market cap data for (e.g., 'ethereum').
Input the pool_address for the Uniswap liquidity pool you wish to analyze.

Running the Script:

Open a terminal or command prompt.
Navigate to the project directory.
Execute the script by running python main_script.py.
The script will output analysis results directly to the terminal and generate visualizations as image files in the project directory. 

Functions Overview:

get_daily_spot_data: Fetches daily OHLC data from Binance for a given cryptocurrency pair.
getDailyVol: Calculates daily volatility from close prices.
get_market_cap: Fetches daily market cap data for a given cryptocurrency from CoinGecko.
fetch_pool_data_to_dataframe: Fetches liquidity pool data from Uniswap for a specified pool.
picture_out: Generates and saves a line plot visualization for a given data column.
corr_matrix: Generates correlation matrix.
main_output: Orchestrates the fetching, processing, and analysis of data, and returns processed DataFrames.
Visualization:
The project generates line plot visualizations for selected columns such as volume, daily volatility, market cap, and liquidity, providing a graphical representation of the data over time.

Data Analysis:

The script includes functionality for scaling selected features, calculating daily volatility and return rates, and combining features into a single composite metric for analysis.
