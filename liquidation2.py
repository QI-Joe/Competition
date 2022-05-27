from black import diff
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


tarpath = r"maker.liquidation.2.20220403.csv"


def read():
    tarFile = pd.read_csv(tarpath)
    return tarFile


def dataProcess():
    target = read()

    takeBlockTime = pd.to_datetime(target.take_block_time, format="%Y/%m/%d %H:%M:%S")
    auctionStartBlockTime = pd.to_datetime(
        target.auction_start_block_time, format="%Y/%m/%d %H:%M:%S"
    )

    differ = takeBlockTime - auctionStartBlockTime
    differ /= np.timedelta64(1, "m")
    differ = differ.rename("differ")

    startTime = auctionStartBlockTime.dt.strftime("%y-%m")
    startTime = startTime.rename("start_time")

    differDF = pd.concat([startTime, differ], axis=1)
    differDF.set_index("start_time", inplace=True)

    differDF = differDF.groupby("start_time").mean()

    return differDF.sort_index()


def plotDraw():
    result = dataProcess()
    print(result)

    fig, ax = plt.subplots()
    ax.bar(result.index, result.differ)
    ax.set_title("liquidation2 time differ")
    plt.show()


if __name__ == "__main__":
    plotDraw()
