import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import numpy as np

liq1Path : str = r"maker.liquidation.1.20220403.csv" 
liq2Path : str = r"maker.liquidation.2.20220403.csv"

def read(inputPath : str):
    tarfile = pd.read_csv(inputPath)
    return tarfile

def DataProcess_Liq1():
    target = read(liq1Path)
    features : pd.DataFrame = pd.DataFrame([pd.to_datetime(target.deal_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m"),  
            pd.to_datetime(target.kick_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m"), 
            pd.to_datetime(target.tend_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m")]).T
    bidPrice = pd.DataFrame(
            { "kick" : pd.to_datetime(target.kick_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m"),
             "collateral_unit" : target.collateral_unit,
            "collateral_type" : target.collateral_type, 
            "dent_lot" : target.dent_lot,
            "tend_bid_dai" : target.tend_bid_dai})
    features = features.dropna(axis=0, how="all")
    bidPrice = bidPrice.dropna(axis=0, how="any")
    bidPrice = bidPrice[bidPrice["collateral_type"] == "ETH-A"]
    return bidPrice, features

def DrawLiq1():
    bidpeice, features = DataProcess_Liq1()
    frequency = [features[item].value_counts().sort_index() for item in features]
    x1Index = frequency[1].index.values.tolist()
    width = 0.4
    # x = date2num(pd.to_datetime(frequency[0].index.values.tolist(), format = "%y-%m"))
    # x1 = date2num(pd.to_datetime(frequency[1].index.values.tolist(), format = "%y-%m"))
    # x2 = date2num(pd.to_datetime(frequency[2].index.values.tolist(), format = "%y-%m"))
    
    x = [item - width for item in range(len(frequency[1]))]
    x1 = [item for item in range(len(frequency[1]))]
    x2 = [item + width for item in range(len(frequency[1]))]
    #-----------------bidprice---------------
    bidpeice.set_index(bidpeice["kick"], drop=True)
    res = bidpeice.groupby(bidpeice["kick"]).sum()
    fig, ax = plt.subplots()
    ax.bar(x, frequency[0], width, color = 'tomato')
    ax.bar(x1, frequency[1], width, color = "slateblue")
    ax.bar(x2, frequency[2], width, color = "forestgreen")
    # ax.xaxis_date()
    ax.plot(x1Index, res["collateral_unit"].div(frequency[1]).mul(40), color = "darkorange", marker = "o", linestyle = "dashed")
    ax.plot(x1Index, res["dent_lot"].div(frequency[1]).mul(40), color = "slategrey", marker = "s", linestyle = "dashed")
    ax.plot(x1Index, res["tend_bid_dai"], color = "fuchsia", marker = "p", linestyle = "dotted")
    plt.legend(["Deal", "Kick", "Tend", "40 times Avg collateral_unit", "40 times Avg dent_lot", "Total tendDai"])
    plt.title("Liqudation 1")
    plt.show()

def DataProcess_Liq2():
    target2 = read(liq2Path)
    features2 : pd.DataFrame = pd.DataFrame([pd.to_datetime(target2.take_block_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m"),  
            pd.to_datetime(target2.auction_start_block_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m")]).T
    bidprice = pd.DataFrame(
        { "StartTime" : pd.to_datetime(target2.take_block_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m"),
            "CollteralType" : target2.symbol,
            "StartPrice/Dai" : target2.starting_price_dai_per_collateral,
            "CollateralPrice/Dai" : target2.price_dai_per_collateral
        }
    )
    features2 = features2.dropna(axis=0, how="all")
    bidprice = bidprice.dropna(axis=0, how="any")
    bidprice = bidprice[bidprice["CollteralType"] == "ETH-A"]
    return bidprice, features2

def DrawLiq2():
    bidp, features2 = DataProcess_Liq2()
    frequency2 = [features2[item].value_counts().sort_index() for item in features2]
    x1Index = frequency2[0].index.values.tolist()
    #-------------bidp processing-----------
    bidp.set_index(bidp["StartTime"], drop=True)
    res = bidp.groupby(bidp["StartTime"]).sum()
    width = 5
    x = date2num(pd.to_datetime(frequency2[0].index.values.tolist(), format = "%y-%m"))
    x1 = date2num(pd.to_datetime(frequency2[1].index.values.tolist(), format = "%y-%m"))
    ax = plt.subplot(2, 1, 1)
    ax.bar(x, frequency2[0], width, color = 'tomato')
    ax.bar(x1+width, frequency2[1], width, color = "slateblue")
    ax.xaxis_date()
    plt.legend(["Take", "Auction"])
    plt.title("Liqudation 2")
    ax1 = plt.subplot(2, 1, 2)
    ax1.plot(x1Index, res["StartPrice/Dai"], marker = "p", color = "teal", linestyle = "-")
    ax1.plot(x1Index, res["CollateralPrice/Dai"], marker = "s", color = "violet", linestyle = "dashed")
    plt.legend(["starting_price_dai_per_collateral", "price_dai_per_collateral"])
    plt.title("Total Price sheet")
    plt.show()

if __name__ == "__main__":
    DrawLiq1()
    DrawLiq2()