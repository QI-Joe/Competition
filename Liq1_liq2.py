import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import numpy as np

liq1Path : str = r"maker.liquidation.1.20220403.csv" 
liq2Path : str = r"maker.liquidation.2.20220403.csv"

def read(inputPath : str):
    tarfile = pd.read_csv(inputPath)
    return tarfile

def New_DataProcess_Liq1():
    target = read(liq1Path)
    target = target[target["collateral_type"] == "ETH-A"]
    features : pd.DataFrame = pd.DataFrame({"deal" : pd.to_datetime(target.deal_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce'),  
            "kick" : pd.to_datetime(target.kick_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce'), 
            "tend" : pd.to_datetime(target.tend_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce'), 
             "fre" : [1 for _ in range(target.kick_time.shape[0])]})
    bidPrice = pd.DataFrame(
            { "kick" : pd.to_datetime(target.kick_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce'),
            "collateral_type" : target.collateral_type, 
            "collateral_unit" : target.collateral_unit,
            "dent_lot" : target.dent_lot,
            "tend_bid_dai" : target.tend_bid_dai,
            "tblknum" : target.tend_block_number,
            "cblknum" : target.call_block_number})
    features = features.dropna(axis=0, how="any")
    bidPrice = bidPrice.dropna(axis=0, how="any")
    return bidPrice, features

def New_DrawLiq1():
    bidprice, fea = New_DataProcess_Liq1()
    Kfea = fea.resample("W-Mon", on = "kick").sum().reset_index().sort_values(by="kick")
    Dfea = fea.resample("W-Mon", on = "deal").sum().reset_index().sort_values(by="deal")
    Tfea = fea.resample("W-Mon", on = "tend").sum().reset_index().sort_values(by="tend")
    blkdiff = np.diff(bidprice.tblknum)
    bidprice.tblknum = np.insert(blkdiff, 0, 0)
    blkdiff = np.diff(bidprice.cblknum)
    bidprice.cblknum = np.insert(blkdiff, 0, 0)
    bidp = bidprice.resample("W-Mon", on = "kick").sum().reset_index().sort_values(by="kick")
    
    dates = date2num(Kfea.kick)
    width = np.diff(dates).min()
    fig, (ax, ax1) = plt.subplots(2)
    ax.bar(dates-width/3, Kfea.fre, facecolor = "slateblue", edgecolor = "white", width=width/3)
    ax.bar(dates, Dfea.fre, facecolor = "orange", edgecolor = "white", width = width/3)
    ax.bar(dates + width/3, Tfea.fre, facecolor = "gold", edgecolor = "white", width = width/3)
    ax.legend(["event Kick amount per week", "event Deal amount per week", "event Tend amount per week"])
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
    ax1.plot(dates, bidp.iloc[:, 1:4])
    ax1.plot(dates, bidp.tblknum, linestyle = "dashed")
    ax1.fill_between(dates, bidp.cblknum, bidp.tend_bid_dai, facecolor = "lavender", edgecolor = "white", alpha = 0.5)
    plt.legend(["Total collateral_unit per week", "Total dent_lot per week", "Total tend_bid_dai per week", "tend_block_number mined difference", "call_block_number mined difference"])
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['bottom'].set_color('#DDDDDD')
    #------hide x ticks----
    ax1.tick_params(bottom=False, left=False)
    # draw horzonal lines from every y value
    ax1.set_axisbelow(True)
    ax1.yaxis.grid(True, color='moccasin')
    ax1.xaxis.grid(False)
    # -----------x axis has too many values.....
    plt.tick_params(axis="x", which = "major", labelsize = 5)
    ax.xaxis_date()
    ax1.xaxis_date()
    plt.show()

def Advacned_Liq2(Liq1path : str = liq1Path, Liq2path : str = liq2Path):
    q1tar, q2tar = read(Liq1path), read(Liq2path)
    q1tar, q2tar = q1tar.dropna(axis=0, how="any"), q2tar.dropna(axis=0, how="any")
    q1tar, q2tar = q1tar[q1tar.collateral_type == "ETH-A"], q2tar[q2tar.symbol == "ETH-A"]
    q1index, q2index = pd.to_datetime(q1tar.kick_time, format="%Y/%m/%d %H:%M:%S", errors='coerce').dt.strftime("%y-%m-%d"), pd.to_datetime(q2tar.take_block_time, format="%Y/%m/%d %H:%M:%S", errors='coerce').dt.strftime("%y-%m-%d")
    q1tar, q2tar = q1tar.select_dtypes(include = [np.float64]), q2tar.select_dtypes(include = [np.float64, np.int64])
    q1tar.set_index(q1index, inplace = True)
    # ------------------set different index to q2 dataset--------------------------
    q2tar = pd.concat([q2tar, pd.to_datetime(q2index, format="%y-%m-%d")], axis=1)
    q2auction_block_number = np.diff(q2tar.auction_block_number)
    q2tar.auction_block_number = np.insert(q2auction_block_number, 0, 0)
    q2tar : pd.DataFrame = q2tar.resample("W-Mon", on="take_block_time").sum().reset_index().sort_values(by = "take_block_time")
    #--------------------starting drawing------------------------------------------------
    fig, (ax, ax1) = plt.subplots(2)
    dates = date2num(q2tar.take_block_time)
    width = np.diff(dates).min()
    ax.fill_between(dates, y1 = q2tar.dai_paid, y2=0, facecolor = "thistle", edgecolor = "white", alpha = 0.7)
    ax1.fill_between(dates, y1 = q2tar.auction_block_number.mul(-1)  , facecolor = "turquoise", edgecolor = "white", alpha = 0.7)
    #----------------------------
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['bottom'].set_color('#DDDDDD')
    #------hide x ticks----
    ax.tick_params(bottom=False, left=False)
    ax1.tick_params(bottom=False, left=False)
    # draw horzonal lines from every y value
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='moccasin')
    ax.xaxis.grid(False)
    ax.xaxis_date()
    ax1.set_axisbelow(True)
    ax1.yaxis.grid(True, color='moccasin')
    ax1.xaxis.grid(False)
    ax1.xaxis_date()
    ax.legend(["Dai Paid(total)"]) 
    ax1.legend(["mined block difference"])
    plt.title("Liqudation 2 analysis data")
    plt.show()



# Hey, remember to implement this is needed
def  DataProcess_Liq1():
    bidp : pd.DataFrame
    fea : pd.DataFrame
    return bidp, fea

def old_DrawLiq1():
    bidpeice, features = DataProcess_Liq1()
    frequency = [features[item].value_counts().sort_index() for item in features]
    x1Index = frequency[1].index.values.tolist()
    width = 0.4
    
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
    New_DrawLiq1()
    Advacned_Liq2()
    DrawLiq2()
