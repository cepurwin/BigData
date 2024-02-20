def filterEasterEggs(dataframes):
    for name, (df, attrs) in dataframes.items():
        condition = df.map(lambda cell: isinstance(cell, bytes) and cell == b'Easteregg :)' or isinstance(cell, str) and cell == 'Easteregg :)')
        rows_to_drop = condition.any(axis=1)

        df.drop(df[rows_to_drop].index, inplace=True)
    return dataframes
