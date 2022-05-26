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

def plotdrawing_Days():
    Pbid, features = dataProcess()
    features = pd.DataFrame(features).T
    frequence = [features[item].value_counts().sort_index() for item in features]
    x = frequence[0].index.values.tolist()
    x = [pd.to_datetime(items, format="%Y-%m-%d") for items in x]
    x1 = frequence[1].index.values.tolist()
    x1 = [pd.to_datetime(items, format="%Y-%m-%d") for items in x1]
    x2 = frequence[2].index.values.tolist()
    x2 = [pd.to_datetime(items, format="%Y-%m-%d") for items in x2]
    frequence = [features[item].value_counts().sort_index().to_numpy().astype(int) for item in features]
    plt.figure(figsize=(10, 10))
    plt.plot(x, frequence[0], color = 'lightcoral')
    plt.plot(x1, frequence[1], color = "royalblue")
    plt.plot(x2, frequence[2], color = "forestgreen")
    plt.legend(["Kick", "Tend", "Deal"])
    plt.show()
    
def plotDraw_Months():
    Pbid, features = dataProcess()
    
    
plotdrawing_Days()
