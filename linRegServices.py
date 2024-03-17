import pandas as pd
from sklearn.linear_model import LinearRegression

def clean_magnetization_with_linReg(dataframes):
    for name, (df, attrs) in dataframes.items():
        # Umwandeln timestamp in Unix
        df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%dT%H:%M:%S").astype('int64') // 10 ** 9
        X = df['timestamp'].values.reshape(-1, 1)  # Wenn 'timestamp' eine Spalte ist
        Y = df['magnetization'].values

        # Lineare Regression instanziieren und anpassen
        lin_reg = LinearRegression()
        lin_reg.fit(X, Y)

        # Berechnung der Residuen
        residuale = Y - lin_reg.predict(X)

        # Anpassung des Mittelwerts der Residuen, um die ursprüngliche Basislinie zu erhalten
        adjusted_residuale = residuale + Y.mean()

        df['magnetization'] = adjusted_residuale

        # Umwandeln des Timestamps zurück in datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime("%Y-%m-%dT%H:%M:%S")

    print("----- Lineare Regressionsberechnung für magnetization fertig -----")
    return dataframes
