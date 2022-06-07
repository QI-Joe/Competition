import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

depositePath : str = r"D:\Study\Web3Work\competition_related\maker.collateral.deposit.20220403.csv"
borrowPath : str = r"D:\Study\Web3Work\competition_related\maker.collateral.borrow.20220403.csv"
repayPath : str = r"D:\Study\Web3Work\competition_related\maker.collateral.repay.20220403.csv"
withdrawPath : str  = r"D:\Study\Web3Work\competition_related\maker.collateral.withdraw.20220403.csv"

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
    # -----------to get time? no, to get Coin type--------------------
    depcoin, wircoin = depfea[depotarget.symbol == "WETH"].resample("W-Mon", on="block_time").sum().reset_index().sort_values(by = "block_time"), witfea[withtarget.symbol == "WETH"].resample("W-Mon", on="block_time").sum().reset_index().sort_values(by = "block_time")
    depres, witres = depfea.resample("W-Mon", on="block_time").sum().reset_index().sort_values(by = "block_time"), witfea.resample("W-Mon", on="block_time").sum().reset_index().sort_values(by = "block_time")
    #----------------basic data transalation has been finshed...--------------------------------------------
    timeFre : pd.DataFrame = pd.concat({"depBlkF" : depres.fre, 
                "witBlkF" : witres.fre, 
                "TimeDiff" : depres.fre.sub(witres.fre)}, axis=1)
    bidFre : pd.DataFrame = pd.concat({"depCou" : depcoin.collateral_unit, 
        "witCou" : wircoin.collateral_unit, 
        "CouDiff" : depcoin.collateral_unit.sub(wircoin.collateral_unit)}, axis=1)
    fig, ax = plt.subplots()
    dates = date2num(depres.block_time)   # np.arange(depres.block_time.size)   tick_label = depres.block_time.dt.strftime("%y-%m-%d")
    width = np.diff(dates).min()
    ax.bar(dates, +timeFre.depBlkF, facecolor = "slateblue", edgecolor = "white", label = "deposit block time", width=width)
    ax.bar(dates, -timeFre.witBlkF, facecolor = "orange", edgecolor = "white", label = "withdrawl block time", width=width)
    ax.plot(dates, timeFre.TimeDiff, label = "Mined Time Difference", color = "red", linestyle = "dashed")
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
    ax.set_yticklabels([str(abs(x)) for x in ax.get_yticks()])
    plt.tick_params(axis="x", which = "major", labelsize = 5)
    fig.autofmt_xdate(rotation = 90)
    ax.xaxis_date()
    plt.legend(["Number Difference", "deposit event number per week", "withdrawl event number per week"])
    plt.title("Chart for deposit and withdraw")
    #-----------draw plots bid price----------------------------------------------
    big, bx = plt.subplots()
    bx.fill_between(dates, bidFre.depCou, 0, facecolor = "tomato", edgecolor = "white", alpha = 0.7)
    bx.fill_between(dates, -bidFre.witCou, 0, facecolor = "gold", edgecolor = "white", alpha = 0.7)
    bx.plot(dates, abs(bidFre.depCou.sub(bidFre.witCou)), color = "darkblue", linestyle = "dashed")
    big.autofmt_xdate(rotation = 45)
    bx.xaxis_date()
    bx.spines['top'].set_visible(False)
    bx.spines['right'].set_visible(False)
    bx.spines['left'].set_visible(False)
    bx.spines['bottom'].set_color('#DDDDDD')
    #------hide x ticks----
    bx.tick_params(bottom=False, left=False)
    #---------------draw horzonal lines from every y value
    bx.set_axisbelow(True)
    bx.yaxis.grid(True, color='moccasin')
    bx.xaxis.grid(False)
    bx.set_yticklabels([str(abs(x)) for x in bx.get_yticks()])
    bx.legend(["WEth deposite collateral unit per week", "WEth withdraw collateral unit per week", "Collateral unit difference"])
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
    ax.set_yticklabels([str(abs(x)) for x in ax.get_yticks()])
    ax.xaxis_date()
    plt.legend([ "Number Different", "repay amount per week", "withdraw amount per week"])
    plt.title("Chart for borrow and repay")
    bider_liq2(bidFre, dates)
    
    #-----------------for bid price --------------------------------------------------
def bider_liq2(bidFre, dates):
    bidFre = pd.concat([bidFre, pd.DataFrame({"culumulate" : [bidFre.CouDiff.loc[0: i].sum() for i  in range(bidFre.CouDiff.shape[0] )]  })   ], axis=1)
    big, (bx, bx1) = plt.subplots(2)
    bx.fill_between(dates, y1 = +bidFre.borCou, y2=0, facecolor = "gold", edgecolor = "white", alpha = 0.7)
    bx.fill_between(dates, y1= 0, y2=-bidFre.repCou, facecolor = "powderblue", edgecolor = "white", alpha = 0.7)
    bx.plot(dates, bidFre.CouDiff, color = "tomato", linestyle = "dashed")
    bx1.fill_between(dates, bidFre.culumulate, facecolor = "orchid", edgecolor = "white", alpha = 0.7)
    #----------------------------------------
    bx.spines['top'].set_visible(False)
    bx.spines['right'].set_visible(False)
    bx.spines['left'].set_visible(False)
    bx.spines['bottom'].set_color('#DDDDDD')
    bx.get_yticklabels([str(abs(x)) for x in bx.get_yticks()])
    bx1.spines['top'].set_visible(False)
    bx1.spines['right'].set_visible(False)
    bx1.spines['left'].set_visible(False)
    bx1.spines['bottom'].set_color('#DDDDDD')
    #------hide x ticks----
    bx.tick_params(bottom=False, left=False)
    bx1.tick_params(bottom=False, left=False)
    # draw horzonal lines from every y value
    bx.set_axisbelow(True)
    bx.yaxis.grid(True, color='moccasin')
    bx.xaxis.grid(False)
    bx1.xaxis_date()
    bx1.set_axisbelow(True)
    bx1.yaxis.grid(True, color='moccasin')
    bx1.xaxis.grid(False)
    big.autofmt_xdate(rotation = 45)
    bx1.xaxis_date()
    bx.legend(["borrow total collateral", "repay total collateral", "Total Collateral different"])
    bx1.legend(["accumulate Collateral in Market"])
    plt.title("This is collteral different trends of borrow and repay/Dai")
    plt.show()
    
def refixer(original, fixed):
    for data in original.kick:
        if data not in fixed.kick: fixed=fixed.append({"kick" : data,"type": fixed.type.iloc[0], "fre" : 0}, ignore_index = True)
    return fixed.sort_index(0, level = "kick", inplace = False)
    
def dwCoinFre():
    depotarget, withtarget = read(depositePath), read(withdrawPath)
    depcoin : pd.DataFrame = pd.DataFrame({"kick": pd.to_datetime(depotarget.block_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce'), "type": depotarget.symbol, "fre" : [1 for _ in range(depotarget.block_time.shape[0])]})
    withcoin : pd.DataFrame = pd.DataFrame({"kick": pd.to_datetime(withtarget.block_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce'), "type" : withtarget.symbol, "fre": [1 for _ in range(withtarget.block_time.shape[0])]})
    depkeys, withkeys = depotarget.symbol.value_counts(), withtarget.symbol.value_counts()
    depaffirs, witaffirs = [], []
    # tempda, tempwa = "", ""
    for item in range(4):
        staffs, witstaffs = depcoin[depcoin.type == depkeys.index[item]], withcoin[withcoin.type == withkeys.index[item]]
        # if item: staffs, witstaffs = refixer(tempda, staffs), refixer(tempwa, witstaffs)
        # elif not item: tempda, tempwa = staffs, witstaffs
        staffs, witstaffs = staffs.resample("W-Mon", on="kick").sum().reset_index().sort_values(by = "kick"), witstaffs.resample("W-Mon", on="kick").sum().reset_index().sort_values(by="kick")
        depaffirs.append(staffs)
        witaffirs.append(witstaffs)
    #------------data washing---------------------
    for item in range(1,4):
        while depaffirs[item].shape[0]<depaffirs[0].shape[0]:
            depaffirs[item] = depaffirs[item].append({"kick": pd.to_datetime("2022-04-04", format="%Y-%m-%d"), "fre" : 0}, ignore_index = True)
        while witaffirs[item].shape[0]<witaffirs[0].shape[0]:
            witaffirs[item] = witaffirs[item].append({"kick": pd.to_datetime("2022-04-04", format="%Y-%m-%d"), "fre" : 0}, ignore_index = True)
    #-----------data washing ------------------------------
    dates = date2num(depaffirs[0].kick)
    width = np.diff(dates).min()
    #--------------start drawing----------------------
    fig, ax = plt.subplots()
    ax.fill_between(dates, +depaffirs[0].fre, y2 = depaffirs[2].fre, facecolor = "wheat", edgecolor = "white", alpha = 0.7)
    ax.fill_between(dates, -depaffirs[1].fre, y2 = -depaffirs[3].fre, facecolor = "paleturquoise", edgecolor = "white", alpha = 0.7)
    ax.bar(dates, depaffirs[2].fre, facecolor = "navy", edgecolor= "white", width=width)
    ax.bar(dates, -depaffirs[3].fre, facecolor = "coral", edgecolor = "white", width=width)
    # -------------------start drawing------------------------------
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
    ax.set_yticklabels([str(abs(x)) for x in ax.get_yticks()])
    ax.legend(depkeys.index[0:4].to_list())
    plt.title("This is the first four widely used stableCoin in deposit/withdraw")
    ax.xaxis_date()
    # ------------------------drawing repay/borrow chart----------------------------------------
    fig, bx = plt.subplots()
    bx.fill_between(dates, +witaffirs[0].fre, y2 = witaffirs[2].fre, facecolor = "palegreen", edgecolor = "white", alpha = 0.7)
    bx.fill_between(dates, -witaffirs[1].fre, y2 = -witaffirs[3].fre, facecolor = "cornflowerblue", edgecolor = "white", alpha = 0.7)
    bx.bar(dates, witaffirs[2].fre, facecolor = "silver", edgecolor= "white", width=width)
    bx.bar(dates, -witaffirs[3].fre, facecolor = "peachpuff", edgecolor = "white", width=width)
    # -------------------start drawing------------------------------
    bx.spines['top'].set_visible(False)
    bx.spines['right'].set_visible(False)
    bx.spines['left'].set_visible(False)
    bx.spines['bottom'].set_color('#DDDDDD')
    #------hide x ticks----
    bx.tick_params(bottom=False, left=False)
    # draw horzonal lines from every y value
    bx.set_axisbelow(True)
    bx.yaxis.grid(True, color='moccasin')
    bx.xaxis.grid(False)
    bx.set_yticklabels([str(abs(x)) for x in bx.get_yticks()])
    bx.legend(depkeys.index[0:4].to_list())
    plt.title("This is the first four widely used stableCoin in repay/borrow")
    bx.xaxis_date()
    plt.show()

repay_borrowProcessShow()
dwCoinFre()
