# CELA_project
### In the main directory there are all files connected to the data collection.
### In the folder 'Analysis' there are files with the analysis of the data.

There are three python files here: get_figi.py, get_candles.py, get_orderbook.py.

1) get_figi.py to get figi by the ticker;
2) get_candles.py to get the csv file with candles of the stock;
3) get_orderbook.py to get the orderbook of the stock;

And additional .csv files:

1) In stocks.csv there are examples of the most liquid stock on MOEX
2) In creds there are credentials for the proper work
3) In sber / mgnt.csv there is data about the stocks

To work with the files, do as following:
1) Make a Tinkoff token
2) Insert it into the creds.py file
3) run any file you want

If you alrdeady have the csv file, just change the path to it in the Analysis files
