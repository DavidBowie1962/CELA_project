from datetime import datetime, timedelta

from pandas import DataFrame
from ta.trend import ema_indicator
from tinkoff.invest import Client, RequestError, CandleInterval, HistoricCandle
from tinkoff.invest.services import Services

from datetime import datetime, timedelta, date, time
from typing import Optional
import converter as op
import creds
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

figi = 'BBG00QPYJ5H0'

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)




def run():
    try:
        with Client(creds.token) as client:
            dt = datetime(2022, 2, 25)
            r = client.market_data.get_candles(
                figi='BBG00QPYJ5H0', #moex
                from_=datetime(2022, 2, 20, 0, 0, 0, 0),
                to=datetime(2022, 2, 23, 00, 0, 0, 0),
                interval=CandleInterval.CANDLE_INTERVAL_HOUR  # см. utils.get_all_candles
            )
            q = client.market_data.get_candles(
                figi='BBG005DXJS36', #spb
                from_=datetime(2022, 2, 20, 0, 0, 0, 0),
                to=datetime(2022, 2, 23, 00, 0, 0, 0),
                interval=CandleInterval.CANDLE_INTERVAL_HOUR  # см. utils.get_all_candles
            )
            print(r)
            # https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#ta.trend.ema_indicator

            ##############################################
            # obtain useable form of money from candles
            def cast_money(v):
                return (v.units + v.nano / 1e9)  # nano - 9 нулей

            # obtain the usd exchange rate to convert rub to usd
            u = client.market_data.get_last_prices(figi=['USD000UTSTOM'])
            usdrur = cast_money(u.last_prices[0].price)

            # создать кастомный data frame для работы с данными
            def create_df_rub(candles: [HistoricCandle]):
                df = DataFrame([{
                    'time': c.time,
                    'volume': round(c.volume / usdrur, 2),
                    'open': round(cast_money(c.open) / usdrur, 2),
                    'close': round(cast_money(c.close) / usdrur, 2),
                    'high': round(cast_money(c.high) / usdrur, 2),
                    'low': round(cast_money(c.low) / usdrur, 2),
                } for c in candles])

                return df

            def create_df(candles: [HistoricCandle]):
                df = DataFrame([{
                    'time': c.time,
                    'volume': c.volume,
                    'open': cast_money(c.open),
                    'close': cast_money(c.close),
                    'high': cast_money(c.high),
                    'low': cast_money(c.low),
                } for c in candles])

                return df

            #df = create_df_rub(r.candles)

            #result = pd.merge(left=df, right=df2, how='outer', left_on='time', right_on='time')
            #result.to_csv('out.csv', sep=',')

            df = create_df_rub(r.candles)

            df2 = create_df(q.candles)
            #########################################################################
            #print(df.head())


            # merging two dataframes to build a plot
            result = pd.merge(left=df, right=df2, how='outer', left_on='time', right_on='time')

            #result.fillna(0)



            #result.index('time')

            # difference of the close_x of the day and the previous one
            result['change_x'] = result.close_x.pct_change()*100
            #print(result['change_x'])
            result['change_y'] = result.close_y.pct_change()*100
            #print(result['change_y'])
            #result = result.dropna()

            """import math
            for i in range(1, len(result['close_x'])):
                if math.isnan(result['close_x'][i]):
                    result['close_x'][i] = result['close_x'][i - 1]
            for i in range(1, len(result['close_y'])):
                if math.isnan(result['close_y'][i]):
                    result['close_y'][i] = result['close_y'][i - 1]"""



            values = result['close_x'].astype(np.double)
            values2 = result['close_y'].astype(np.double)
            mask = np.isfinite(values)
            mask2 = np.isfinite(values2)


            #result = result.set_index(['time'])
            #print(result.head())
            #result['close_x'][mask].plot(label='moex')
            #result['close_y'][mask2].plot(label='spb')
            #plt.plot(result['time'], result['close_x'][np.isfinite(result['close_x'])], label='Darova')
            plt.plot(result['time'][mask], result['close_x'][mask].fillna(method='ffill'), label='moex')
            plt.plot(result['time'][mask2], result['close_y'][mask2].fillna(method='ffill'), label='spb')
            plt.legend()
            plt.gcf().autofmt_xdate()
            plt.title("result")
            plt.show()



            # save the result df to csv
            #result = result.fillna(method='ffill')
            #result.to_csv('out.csv', sep=',')
            #print(result.head(20))

            #print(df)
            df = df.set_index(['time'])
            df2 = df2.set_index(['time'])
            #print(df)
            df['close'].plot(label='moex')
            df2['close'].plot(label='spb')
            plt.legend()
            plt.title("df df2")
            plt.show()





            y = result['change_x']
            y1 = result['change_y']
            #x = result['time']
            #ax3 = plt.subplot()
            #ax3.plot(x, y, label='moex')
            #ax3.plot(x, y1, label='sbp')
            #ax3.legend()
            #plt.gcf().autofmt_xdate()
            #plt.show()


            y1 = result['close_x']
            y2 = result['close_y']
            #x = result['time']
            #ax = plt.subplot()
            #plt.plot(x, y1, x, y2)
            #ax.plot(x, y1, label='moex')
            #ax.plot(x, y2, label='sbp')
            #ax.legend()
            #plt.title('result')
            #plt.gcf().autofmt_xdate() #форматирование даты

            #plt.show()

            #sns.relplot(x=x, y=y2, hue=result['volume_y'],
                        #kind="line", data=result)
            #ax2.plot(x, x3, label='volume')
            #sns.relplot(x=x, y=y1, size=x3,
                        #sizes=(4, 400), alpha=.5, palette="muted",
                        #height=6, data=result)

            # https://plotly.com/python/candlestick-charts/
            """fig = go.Figure(data=[go.Candlestick(x=result['time'],
                                                 open=result['open_x'],
                                                 high=result['high_x'],
                                                 low=result['low_x'],
                                                 close=result['close_x'])])"""

            #fig.show()
            #plt.show()







    except RequestError as e:
        print(str(e))


run()