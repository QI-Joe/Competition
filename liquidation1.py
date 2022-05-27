from black import diff
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


tarpath = r"maker.liquidation.1.20220403.csv"


def read():
    tarFile = pd.read_csv(tarpath)
    return tarFile


def dataProcess():
    target = read()

    dealTime = pd.to_datetime(target.deal_time, format="%Y/%m/%d %H:%M:%S")
    kickTime = pd.to_datetime(target.kick_time, format="%Y/%m/%d %H:%M:%S")

    tendTime = pd.to_datetime(target.tend_time, format="%Y/%m/%d %H:%M:%S")
    dentTime = pd.to_datetime(target.dent_time, format="%Y/%m/%d %H:%M:%S")

    dealDiffer = dealTime - kickTime
    dealDiffer /= np.timedelta64(1, "m")
    dealDiffer = dealDiffer.rename("deal_differ")

    tendDiffer = tendTime - kickTime
    tendDiffer /= np.timedelta64(1, "m")
    tendDiffer = tendDiffer.rename("tend_differ")

    dentDiffer = dentTime - kickTime
    dentDiffer /= np.timedelta64(1, "m")
    dentDiffer = dentDiffer.rename("dent_differ")

    startTime = kickTime.dt.strftime("%y-%m")

    differDF = pd.concat([startTime, dealDiffer, tendDiffer, dentDiffer], axis=1)
    differDF.set_index("kick_time", inplace=True)

    differDF = differDF.groupby("kick_time").mean()

    return differDF.sort_index()


def plotDraw():
    result = dataProcess()
    print(result)

    fig, ax = plt.subplots()
    ax.bar(result.index, result.deal_differ)
    ax.set_title("liquidation1 deal time differ")
    plt.show()

    fig, ax = plt.subplots()
    ax.bar(result.index, result.tend_differ)
    ax.set_title("liquidation1 tend time differ")
    plt.show()

    fig, ax = plt.subplots()
    ax.bar(result.index, result.dent_differ)
    ax.set_title("liquidation1 dent time differ")
    plt.show()


if __name__ == "__main__":
    plotDraw()
