from sqlite3 import DatabaseError
from turtle import color
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

def deposite_withdrawProcessShow(Path : str) :
    target = read(Path)
    features : pd.DataFrame = pd.DataFrame([pd.to_datetime(target.block_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m"),  
       target.collateral_unit]).T
    features = features.dropna(axis=0, how="all")
    # elimate all Non value
    frequency = features["block_time"].value_counts().sort_index()
    x1Index = frequency.index.values.tolist()
    features.set_index(features["block_time"], drop=True, inplace=True)
    result = features.groupby(level=0).sum()
    result = pd.DataFrame({"Frequency" : frequency, "collateral" : result["collateral_unit"].div(frequency)})
    x = date2num(pd.to_datetime(x1Index, format="%y-%m"))
    width = 15
    name : str = "Withdraw"
    if "deposit" in Path: name = "Deposit"
    ax = plt.subplot(2, 1, 1)
    plt.bar(x, result["Frequency"], width, color = "slateblue")
    ax.xaxis_date()
    plt.title("{} Frequency of Block_time".format(name))
    plt.subplot(2, 1, 2)
    plt.plot(x1Index, result["collateral"], color = "darkorange", marker = "o", linestyle = "dashed")
    plt.title("{} Avg monthly collateral".format(name))
    plt.show()

def repay_borrowProcessShow(Path : int):
    target = read(borrowPath)
    features : pd.DataFrame = pd.DataFrame([pd.to_datetime(target.block_time, format = '%Y/%m/%d %H:%M:%S', errors='coerce').dt.strftime("%y-%m"),  
       target.dai_unit]).T
    features = features.dropna(axis=0, how="all")
    # elimate all Non value
    frequency = features["block_time"].value_counts().sort_index()
    x1Index = frequency.index.values.tolist()
    features.set_index(features["block_time"], drop=True, inplace=True)
    result = features.groupby(level=0).sum()
    result = pd.DataFrame({"Frequency" : frequency, "dai" : result["dai_unit"].div(frequency)})
    x = date2num(pd.to_datetime(x1Index, format="%y-%m"))
    width = 15
    name = "Repay"
    if "borrow" in Path : name = "Borrow"
    ax = plt.subplot(2, 1, 1)
    plt.bar(x, result["Frequency"], width, color = "slateblue")
    ax.xaxis_date()
    plt.title("{} Frequency of Block_time".format(name))
    plt.subplot(2, 1, 2)
    plt.plot(x1Index, result["dai"], color = "darkorange", marker = "o", linestyle = "dashed")
    plt.title("{} Avg monthly Dai".format(name))
    plt.show()

deposite_withdrawProcessShow(depositePath)