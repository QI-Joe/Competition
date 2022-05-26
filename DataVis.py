import pandas as pd
import matplotlib.pyplot as plt

tarpath = r""
def read():
    tarfile = pd.read_csv(tarpath)
    return tarfile

def dataProcess():
    target : pd.Series = read()
    features : list= [pd.to_datetime(target.deal_time, format = '%m/%d/%Y %H:%M:%S').dt.strftime("%Y-%m-%d"), 
                      pd.to_datetime(target.kick_time, format = '%m/%d/%Y %H:%M:%S').dt.strftime("%Y-%m-%d"), 
                      pd.to_datetime(target.tend_time, format = '%m/%d/%Y %H:%M:%S').dt.strftime("%Y-%m-%d")]
    return target.bid_price_unit_of_mkr, features

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
    avg = result["bid_price_unit_of_mkr"].div(frequency[1])
    fig, ax = plt.subplots()
    # fig(figsize=(10, 10))
    ax.bar(x, frequency[0], width, color = 'tomato')
    ax.bar(x1, frequency[1], width, color = "slateblue")
    ax.bar(x2, frequency[2], width, color = "forestgreen")
    ax.plot(x1Index, avg, color = "darkorange", marker = "o", linestyle = "dashed")
    plt.legend(["Avg Monthly Price", "Deal", "Kick", "Tend"])
    # #------------------------
    # plt.subplot(2, 2, 1)
    # plt.plot(x, frequency[0], color = 'lightcoral', marker = "o")
    # plt.legend(["Deal"])
    # #------------------------
    # plt.subplot(2, 2, 2)
    # plt.plot(x1, frequency[1], color = "royalblue", linestyle = "--")
    # plt.legend(["Kick"])
    # #------------------------
    # plt.subplot(2, 2, 3)
    # plt.plot(x2, frequency[2], color = "forestgreen", label = "Deal")
    # plt.legend(["Tend"])
    # #--------------------------
    # plt.subplot(2, 2, 4)
    
    plt.show()
    
plotDraw_Months()
