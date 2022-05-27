import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

tarpath = r"C:\Users\Qi Shihao\Desktop\Web3Work\competition_related\maker.liquidation.surplus.20220403.csv"
def read(inputPath : str):
    tarfile = pd.read_csv(inputPath)
    return tarfile

def TimeDiffdataProcess():
    target : pd.Series = read(tarpath)
    features : list= [pd.to_datetime(target.deal_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce').dt.strftime("%Y-%m-%d"),  
                        pd.to_datetime(target.kick_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce').dt.strftime("%Y-%m-%d"), 
                        pd.to_datetime(target.tend_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce').dt.strftime("%Y-%m-%d")]
    return target.bid_price_unit_of_mkr, features

def dataProcess():
    target = read()

    id = target.surplus_auction_id
    dealTime = pd.to_datetime(target.deal_time, format="%Y/%m/%d %H:%M:%S")
    kickTime = pd.to_datetime(target.kick_time, format="%Y/%m/%d %H:%M:%S")
    # dentTime = pd.to_datetime(target.dent_time, format="%Y/%m/%d %H:%M:%S")
    dentLot = target.dent_lot

    lastid = id[0]
    lastindex = 0
    result = []
    for index in range(len(id)):
        if id[index] != lastid or index == len(id) - 1:
            # kick_time = kickTime[lastindex].strftime("%Y-%m-%d")

            deal_kick = dealTime[index - 1] - kickTime[lastindex]
            deal_kick /= np.timedelta64(1, "h")

            # deal_dent = dealTime[index - 1] - dentTime[lastindex]
            # deal_dent /= np.timedelta64(1, "h")

            lot_start = dentLot[lastindex]
            lot_ent = dentLot[index - 1]
            lot_differ = lot_start - lot_ent

            result.append((lastid, deal_kick, lot_differ, lot_ent))

            lastid = id[index]
            lastindex = index

    resultDataFrame = pd.DataFrame(
        result,
        columns=["id", "deal_kick", "lot_differ", "lot_end"],
    )
    resultDataFrame.set_index("id", drop=True, inplace=True)

    return resultDataFrame


def plotDraw():
    result = TimeDiffdataProcess()
    fig, ax = plt.subplots()
    ax.plot(result.index, result.deal_kick)
    ax.set_title("deal - kick")

def plotDraw2():
    result = TimeDiffdataProcess()
    fig, ax = plt.subplots()
    ax.clear()
    ax.plot(result.index, result.lot_differ)
    ax.set_title("lot_differ")
    plt.show()

def plotDraw3():
    result = TimeDiffdataProcess()
    fig, ax = plt.subplots()
    ax.clear()
    ax.plot(result.index, result.lot_end)
    ax.set_title("lot_end")
    plt.show()


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


def plotDraw_Months():
    Pbid, features = dataProcess()
    features = [pd.to_datetime(item, format="%Y-%m-%d").dt.strftime("%y-%m") for item in features]
    #---------------for pbid----merged with kick_time----------------------------
    Pbid = pd.concat([Pbid, features[1]], axis=1)
    Pbid.set_index("kick_time", drop=True, inplace=True)
    result = Pbid.groupby(level=0).sum()
    #-----Hence we get sum of price every month(only suit for kick time) -------------------------
    features = pd.DataFrame(features).T
    frequency = [features[item].value_counts().sort_index() for item in features]
    # x = frequency[0].index.values.tolist()
    x1Index = frequency[1].index.values.tolist()
    # x2 = frequency[2].index.values.tolist()
    width = 0.2
    x = [item - width for item in range(len(frequency[1]))]
    x1 = [item for item in range(len(frequency[1]))]
    x2 = [item + width for item in range(len(frequency[1]))]
    frequency = [features[item].value_counts().sort_index().to_numpy().astype(int) for item in features]
    avg = result["bid_price_unit_of_mkr"].div(frequency[1]).mul(20)
    fig, ax = plt.subplots()
    # fig(figsize=(10, 10))
    ax.bar(x, frequency[0], width, color = 'tomato')
    ax.bar(x1, frequency[1], width, color = "slateblue")
    ax.bar(x2, frequency[2], width, color = "forestgreen")
    ax.plot(x1Index, avg, color = "darkorange", marker = "o", linestyle = "dashed")
    plt.legend(["Avg Monthly Price", "Deal", "Kick", "Tend"])
    
    plt.show()

def DataProcess_Liq1():
    target = read(r"C:\Users\Qi Shihao\Desktop\Web3Work\competition_related\maker.liquidation.1.20220403.csv")
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
DrawLiq1()

def DataProcess_Liq2():
    target2 = read(r"C:\Users\Qi Shihao\Desktop\Web3Work\competition_related\maker.liquidation.2.20220403.csv")
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

DrawLiq2()
