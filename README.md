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
Please note: In some regions, such as the USA, access to the Binance API is restricted. Therefore, you might need to use a proxy to switch to other regions, like Singapore or Japan and etc, for access.

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

Data Analysis:

The script includes functionality for scaling selected features, calculating daily volatility, and combining features into a single composite metric for analysis.
