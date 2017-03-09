"""
Script responsible for processing and visualising user activity data.
"""
import os

import matplotlib.pyplot as plt
import pandas as pd


def sliceMonthly(df):
    """
    Slices the given DataFrame whose index contains dates into monthly chunks.

    :param df: A pandas DataFrame object that contains transaction information.
    :return: A list of DataFrame objects that contain monthly transactions.
    """
    return [df.loc[df.index.month == m] for m in range(1, 13)]


def readData(dataPath, delimiter=","):
    """
    Reads the CSV file containing user activity.

    :param dataPath: Path to the CSV data file.
    :param delimiter: The separator character for the CSV file.
    :return: Pandas DataFrame object containing user activity.
    """
    return pd.DataFrame.from_csv(dataPath,
                                 sep=delimiter,
                                 index_col=False,
                                 infer_datetime_format=True)



# TODO: WORKING ! ! !
# Attempting to graph csv data
def plotUsers(dataPath, outPath):
    """
    """
    plt.style.use('ggplot')

    users = data["USER"].unique()


    fig = plt.figure()
    ax = fig.add_subplot(111)



    # TODO: Fix pandas throwing error
    for user in users:
        df = data[data["USER"] == user]

        df["TIME"] = pd.to_datetime(df["TIME"])
        # df["TIME"] = df["TIME"].dt.strftime("%H%M")
        print(df["TIME"])


        df.plot(x="TIME", y="JOIN", ax=ax, label=user, kind="line")


        ax.set_title("User History")

    print(ax.get_xlim())
    # ax.set_xlim(dt.time(0, 0, 0), dt.time(3, 3, 3))
    ax.set_ylim(-0.5, 1.5)

    plt.show()








dataDir = os.path.join(".", "data")
logPath = os.path.join(dataDir, "log.csv")
plotPath = os.path.join(dataDir, "history.png")
plotUsers(logPath, plotPath)

