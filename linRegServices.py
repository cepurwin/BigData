import pandas as pd
from sklearn.linear_model import LinearRegression

def clean_magnetization_with_linReg(dataframes):
    for name, (df, attrs) in dataframes.items():
        # Umwandeln timestamp in Unix
        df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%dT%H:%M:%S").astype('int64') // 10 ** 9
        # Dies ist nur ein Beispiel, wie es gehen könnte, abhängig von der genauen Struktur deiner Timestamps
        X = df['timestamp'].values.reshape(-1, 1)  #wenn 'timestamp' eine Spalte ist

        # Y ist der Magnetisierungswert
        Y = df['magnetization'].values.reshape(-1, 1)

        # Lineare Regression instanziieren und anpassen
        lin_reg = LinearRegression()
        print(f'Lineare Regression magnetization für: {name}')
        lin_reg.fit(X, Y)

        # Vorhersage der Magnetisierungswerte
        Y_pred = lin_reg.predict(X)

        # Berechnung der Trends ohne den Offset zu entfernen
        Y_trend = (Y_pred - lin_reg.intercept_).flatten()  # Entferne den Achsenabschnitt aus der Vorhersage

        # Korrigiere die ursprünglichen Daten, indem nur der Trend subtrahiert wird
        df['magnetization'] = df['magnetization'] - Y_trend
        # Umwandeln des Timestamps zurück in datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime("%Y-%m-%dT%H:%M:%S")
    print("----- Lineare Regressionsberechnung für magnetization fertig -----")
    return dataframes