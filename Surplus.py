import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import numpy as np

tarpath = r"maker.liquidation.surplus.20220403.csv"

def read(inputPath : str):
    tarfile = pd.read_csv(inputPath)
    return tarfile

def dataProcess():
    target : pd.Series = read(tarpath)
    features : list= [pd.to_datetime(target.deal_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce').dt.strftime("%Y-%m-%d"),  
                        pd.to_datetime(target.kick_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce').dt.strftime("%Y-%m-%d"), 
                        pd.to_datetime(target.tend_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce').dt.strftime("%Y-%m-%d")]
    return target.bid_price_unit_of_mkr, features

def plotdrawing_Days():
    _, features = dataProcess()
    features = pd.DataFrame(features).T
    frequence = [features[item].value_counts().sort_index() for item in features]
    x = [pd.to_datetime(items, format="%Y-%m-%d") for items in frequence[0].index.values.tolist()]
    x1 = [pd.to_datetime(items, format="%Y-%m-%d") for items in frequence[1].index.values.tolist()]
    x2 = [pd.to_datetime(items, format="%Y-%m-%d") for items in frequence[2].index.values.tolist()]
    frequence = [features[item].value_counts().sort_index().to_numpy().astype(int) for item in features]
    plt.figure(figsize=(10, 10))
    plt.plot(x, frequence[0], color = 'lightcoral')
    plt.plot(x1, frequence[1], color = "royalblue")
    plt.plot(x2, frequence[2], color = "forestgreen")
    plt.legend(["Kick", "Tend", "Deal"])
    plt.show()

def dataProcess2():
    target : pd.Series = read(tarpath)
    features : list= [pd.DataFrame({"deal" : pd.to_datetime(target.deal_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce'), "fre" : [1 for _ in range(target.deal_time.shape[0])]}), 
                    pd.DataFrame({"kick" : pd.to_datetime(target.kick_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce'), "fre" : [1 for _ in range(target.kick_time.shape[0])]}), 
                    pd.DataFrame({"tend" : pd.to_datetime(target.tend_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce'), "fre" : [1 for _ in range(target.tend_time.shape[0])]})]
    return target.bid_price_unit_of_mkr, features

def plotDraw_Months():
    Pbid, features = dataProcess2()
    #---------------for pbid----merged with kick_time----------------------------
    Pbid = pd.DataFrame(Pbid).set_index(features[1].kick, inplace = False)
    features = [features[0].resample("W-Mon", on="deal").sum().reset_index().sort_values(by = "deal"), 
                features[1].resample("W-Mon", on="kick").sum().reset_index().sort_values(by = "kick"),
                features[2].resample("W-Mon", on="tend").sum().reset_index().sort_values(by = "tend")]
    Pbid = Pbid.resample("W-Mon").sum().reset_index().sort_values(by="kick")
    dates = date2num(features[1].kick)
    ax = plt.subplot(2, 1, 1)
    ax.bar(dates, features[0].fre, facecolor = "lightseagreen", edgecolor = "white", width = 10)
    ax.bar(dates+10, features[1].fre, facecolor = "orangered", edgecolor = "white", width = 10)
    ax.plot(dates, features[2].fre, color = "blueviolet", linestyle = "dashdot")
    plt.legend(["event tend occur number", "event deal occur number", "event kick occur number"])
    ax1 = plt.subplot(2, 1, 2)
    ax1.plot(dates, Pbid.bid_price_unit_of_mkr, color = "tomato", linestyle = "dashed")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    #------hide x ticks----
    ax.tick_params(bottom=False, left=False)
    # draw horzonal lines from every y value
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='moccasin')
    ax.xaxis.grid(False)
    # -----------x axis has too many values.....
    plt.tick_params(axis="x", which = "major", labelsize = 5)
    ax.xaxis_date()
    ax1.set_axisbelow(True)
    ax1.yaxis.grid(True, color='moccasin')
    ax1.xaxis.grid(False)
    ax1.xaxis_date()
    plt.title("total bid_price_unit_of_mkr")
    plt.show()
   
