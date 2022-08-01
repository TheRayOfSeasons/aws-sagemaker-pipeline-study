import pandas as pd


def extract_dataset(data_source):
    """
    Extracts the X and y sets from the raw data.
    """

    music_dataframe = pd.read_csv(data_source)

    # input set
    # without genre
    X = music_dataframe.drop(columns=['genre']).values

    # output set
    # genre only
    y = music_dataframe['genre']

    return X, y
