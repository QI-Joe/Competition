import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

depositePath : str = r"C:\Users\Qi Shihao\Desktop\Web3Work\competition_related\maker.collateral.deposit.20220403.csv"
borrowPath : str = r"C:\Users\Qi Shihao\Desktop\Web3Work\competition_related\maker.collateral.borrow.20220403.csv"
repayPath : str = r"C:\Users\Qi Shihao\Desktop\Web3Work\competition_related\maker.collateral.repay.20220403.csv"
withdrawPath : str  = r"C:\Users\Qi Shihao\Desktop\Web3Work\competition_related\maker.collateral.withdraw.20220403.csv"

def read(inputPath : str):
    tarfile = pd.read_csv(inputPath)
    return tarfile

def deposite_withdrawProcessShow(depositPath : str = depositePath , withdrawpath : str = withdrawPath) :
    depotarget, withtarget = read(depositPath), read(withdrawpath)
    depfea : pd.DataFrame = pd.DataFrame({"block_time" : pd.to_datetime(depotarget.block_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m-%d %H:%M:%S"),  
       "collateral_unit" : np.float64(depotarget.collateral_unit)})
    witfea : pd.DataFrame = pd.DataFrame({"block_time" : pd.to_datetime(withtarget.block_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m-%d %H:%M:%S"),
        "collateral_unit" : np.float64(withtarget.collateral_unit)})
    depfea, witfea = pd.concat([depfea, pd.DataFrame({"fre" : [1 for _ in range(depfea.shape[0])]})], axis=1), pd.concat([witfea, pd.DataFrame({"fre" : [1 for _ in range(witfea.shape[0])]})], axis=1)
    depfea, witfea = depfea.dropna(axis=0, how="any"), witfea.dropna(axis=0, how="any")
    depfea["block_time"], witfea["block_time"] = pd.to_datetime(depfea.block_time, format = "%y-%m-%d %H:%M:%S"), pd.to_datetime(witfea.block_time, format = "%y-%m-%d %H:%M:%S")
    depres, witres = depfea.resample("W-Mon", on="block_time").sum().reset_index().sort_values(by = "block_time"), witfea.resample("W-Mon", on="block_time").sum().reset_index().sort_values(by = "block_time")
    #----------------basic data transalation has been finshed...--------------------------------------------
    timeFre : pd.DataFrame = pd.concat({"depBlkF" : depres.fre, 
                "witBlkF" : witres.fre, 
                "TimeDiff" : depres.fre.sub(witres.fre)}, axis=1)
    bidFre : pd.DataFrame = pd.concat({ "depCou" : depres.collateral_unit, 
        "witCou" : witres.collateral_unit, 
        "CouDiff" : depres.collateral_unit.sub(witres.collateral_unit)}, axis=1)
    fig, ax = plt.subplots()
    dates = date2num(depres.block_time)   # np.arange(depres.block_time.size)   tick_label = depres.block_time.dt.strftime("%y-%m-%d")
    width = np.diff(dates).min()
    ax.bar(dates, +timeFre.depBlkF, facecolor = "slateblue", edgecolor = "white", label = "deposit block time", width=width)
    ax.bar(dates, -timeFre.witBlkF, facecolor = "orange", edgecolor = "white", label = "withdrawl block time", width=width)
    ax.plot(dates, timeFre.TimeDiff, label = "Mined Time Difference", color = "aquamarine", linestyle = "dashed")
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
    fig.autofmt_xdate(rotation = 90)
    ax.xaxis_date()
    plt.legend(["Mined Time Difference", "deposit block time", "withdrawl block time"])
    plt.title("Chart for deposit and withdraw")
    #-----------draw plots bid price----------------------------------------------
    big, bx = plt.subplots()
    bx.fill_between(dates, y1 = +bidFre.depCou.mul(1e6), y2=0, facecolor = "red", alpha = 0.7)
    bx.fill_between(dates, y1= 0, y2=-bidFre.witCou, facecolor = "powderblue", alpha = 0.7)
    big.autofmt_xdate(rotation = 45)
    bx.xaxis_date()
    plt.show()

def repay_borrowProcessShow(borrowpath : str = borrowPath, repaypath : str = repayPath):
    borotarget, reptarget = read(borrowpath), read(repaypath)
    borfea : pd.DataFrame = pd.DataFrame({"block_time" : pd.to_datetime(borotarget.block_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m-%d %H:%M:%S"),  
       "dai_unit" : np.float64(borotarget.dai_unit)})
    repfea : pd.DataFrame = pd.DataFrame({"block_time" : pd.to_datetime(reptarget.block_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m-%d %H:%M:%S"),
        "dai_unit" : np.float64(reptarget.dai_unit)})
    borfea, repfea = pd.concat([borfea, pd.DataFrame({"fre" : [1 for _ in range(borfea.shape[0])]})], axis=1), pd.concat([repfea, pd.DataFrame({"fre" : [1 for _ in range(repfea.shape[0])]})], axis=1)
    borfea, repfea = borfea.dropna(axis=0, how="any"), repfea.dropna(axis=0, how="any")
    borfea["block_time"], repfea["block_time"] = pd.to_datetime(borfea.block_time, format = "%y-%m-%d %H:%M:%S"), pd.to_datetime(repfea.block_time, format = "%y-%m-%d %H:%M:%S")
    borres, repres = borfea.resample("W-Mon", on="block_time").sum().reset_index().sort_values(by = "block_time"), repfea.resample("W-Mon", on="block_time").sum().reset_index().sort_values(by = "block_time")
    #----------------basic data transalation has been finshed...--------------------------------------------
    timeFre : pd.DataFrame = pd.concat({"borBlkF" : borres.fre, 
                "repBlkF" : repres.fre, 
                "TimeDiff" : borres.fre.sub(repres.fre)}, axis=1)
    bidFre : pd.DataFrame = pd.concat({ "borCou" : borres.dai_unit, 
        "repCou" : repres.dai_unit, 
        "CouDiff" : borres.dai_unit.sub(repres.dai_unit)}, axis=1)
    fig, ax = plt.subplots()
    dates = date2num(borres.block_time)   # np.arange(depres.block_time.size)   tick_label = depres.block_time.dt.strftime("%y-%m-%d")
    width = np.diff(dates).min()
    ax.bar(dates, +timeFre.borBlkF, facecolor = "plum", edgecolor = "white", width=width)
    ax.bar(dates, -timeFre.repBlkF, facecolor = "darkseagreen", edgecolor = "white", width=width)
    ax.plot(dates, timeFre.TimeDiff, color = "orangered", linestyle = "dashed")
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
    fig.autofmt_xdate(rotation = 90)
    ax.xaxis_date()
    plt.legend([ "Mined Time Difference", "deposit block time", "withdraw block time"])
    plt.title("Chart for borrow and repay")
    #-----------------for bid price --------------------------------------------------
    big, bx = plt.subplots()
    bx.fill_between(dates, y1 = +bidFre.borCou, y2=0, facecolor = "gold", edgecolor = "white", alpha = 0.7)
    bx.fill_between(dates, y1= 0, y2=-bidFre.repCou, facecolor = "powderblue", edgecolor = "white", alpha = 0.7)
    bx.plot(dates, bidFre.CouDiff, color = "tomato", linestyle = "dashed")
    #----------------------------------------
    bx.spines['top'].set_visible(False)
    bx.spines['right'].set_visible(False)
    bx.spines['left'].set_visible(False)
    bx.spines['bottom'].set_color('#DDDDDD')
    #------hide x ticks----
    ax.tick_params(bottom=False, left=False)
    # draw horzonal lines from every y value
    bx.set_axisbelow(True)
    bx.yaxis.grid(True, color='moccasin')
    bx.xaxis.grid(False)
    big.autofmt_xdate(rotation = 45)
    bx.xaxis_date()
    plt.legend(["Total Collateral different", "borrow total collateral", "repay total collateral"])
    plt.title("Good, this is collteral different trends of borrow and repay/Dai")
    plt.show()
    
repay_borrowProcessShow()