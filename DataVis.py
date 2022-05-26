import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

tarpath = r"C:\Users\Qi Shihao\Desktop\Web3Work\competition_related\maker.liquidation.surplus.20220403.csv"
def read(inputPath : str):
    tarfile = pd.read_csv(inputPath)
    return tarfile

def dataProcess():
    target : pd.Series = read(tarpath)
    features : list= [pd.to_datetime(target.deal_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce').dt.strftime("%Y-%m-%d"),  
                        pd.to_datetime(target.kick_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce').dt.strftime("%Y-%m-%d"), 
                        pd.to_datetime(target.tend_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce').dt.strftime("%Y-%m-%d")]
    return target.bid_price_unit_of_mkr, features

def DateCalculate():
    target = read(tarpath)
    features : list = [pd.to_datetime(target.deal_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce'),  
                    pd.to_datetime(target.kick_time, format = '%m/%d/%Y %H:%M:%S', errors='coerce')]
    features = pd.DataFrame(features).T
    newfea : pd.DataFrame= (pd.to_datetime(features["deal_time"], format="%m/%d/%Y %H:%M:%S") - pd.to_datetime(features["kick_time"], format="%m/%d/%Y %H:%M:%S"))
    newfea = pd.DataFrame({"time" : newfea})
    newfea = pd.concat([newfea, features["kick_time"]], axis=1)
    newfea["kick_time"] = pd.to_datetime(newfea["kick_time"], format="%m/%d/%Y %H:%M:%S").dt.strftime("%Y-%m-%d")
    newfea.set_index(newfea["kick_time"], drop=True, inplace=True)
    frequency = newfea.groupby(level=0).sum()
    Xindex = frequency.index.values.tolist()
    plt.scatter(Xindex, frequency["time"])
    plt.show()
# new feature
DateCalculate()

"""
The DTypes <class 'numpy.dtype[timedelta64]'> and <class 'numpy.dtype[float64]'> do not have a common DType. 
For example they cannot be stored in a single array unless the dtype is `object`.
"""


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
    features = features.dropna(axis=0, how="all")
    return features

def Draw_liq1():
    features = DataProcess_Liq1()
    frequency = [features[item].value_counts().sort_index() for item in features]
    x1Index = frequency[1].index.values.tolist()
    width = 5
    x = date2num(pd.to_datetime(frequency[0].index.values.tolist(), format = "%y-%m"))
    x1 = date2num(pd.to_datetime(frequency[1].index.values.tolist(), format = "%y-%m"))
    x2 = date2num(pd.to_datetime(frequency[2].index.values.tolist(), format = "%y-%m"))
    
    ax = plt.subplot(1, 1, 1)
    # fig(figsize=(10, 10))
    ax.bar(x-width, frequency[0], width, color = 'tomato')
    ax.bar(x1, frequency[1], width, color = "slateblue")
    ax.bar(x2+width, frequency[2], width, color = "forestgreen")
    ax.xaxis_date()
    plt.legend(["Deal", "Kick", "Tend"])
    plt.title("Liqudation 1")
    plt.show()

def DataProcess_Liq2():
    target2 = read(r"C:\Users\Qi Shihao\Desktop\Web3Work\competition_related\maker.liquidation.2.20220403.csv")
    features2 =  pd.DataFrame = pd.DataFrame([pd.to_datetime(target2.take_block_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m"),  
            pd.to_datetime(target2.auction_start_block_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m")]).T
    features2 = features2.dropna(axis=0, how="all")
    return features2

def DrawLiq2():
    features2 = DataProcess_Liq2()
    frequency2 = [features2[item].value_counts().sort_index() for item in features2]
    x1Index = frequency2[1].index.values.tolist()
    width = 5
    x = date2num(pd.to_datetime(frequency2[0].index.values.tolist(), format = "%y-%m"))
    x1 = date2num(pd.to_datetime(frequency2[1].index.values.tolist(), format = "%y-%m"))
    
    ax = plt.subplot(1, 1, 1)
    # fig(figsize=(10, 10))
    ax.bar(x, frequency2[0], width, color = 'tomato')
    ax.bar(x1+width, frequency2[1], width, color = "slateblue")
    ax.xaxis_date()
    plt.legend(["Take", "Auction"])
    plt.title("Liqudation 2")
    plt.show()

def main():
    DrawLiq2()

