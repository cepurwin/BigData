import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

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

        # Skalierer für die Features und die Zielvariable
        scaler_X = StandardScaler()
        scaler_Y = StandardScaler()

        X_scaled = scaler_X.fit_transform(X)
        Y_scaled = scaler_Y.fit_transform(Y).flatten()

        # Lineare Regression auf skalierte Daten anwenden
        lin_reg.fit(X_scaled, Y_scaled)

        # Vorhersage auf der Basis der skalierten Zeitstempel
        Y_pred_scaled = lin_reg.predict(X_scaled)

        # Rückskalierung der vorhergesagten Werte auf die ursprüngliche Skala der Magnetisierung
        Y_pred = scaler_Y.inverse_transform(Y_pred_scaled.reshape(-1, 1)).flatten()

        # Berechnung der korrigierten Magnetisierungswerte
        df['magnetization'] = Y.flatten() - Y_pred
        print(len(df['magnetization']))

        # Umwandeln des Timestamps zurück in datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime("%Y-%m-%dT%H:%M:%S")
    print("----- Lineare Regressionsberechnung für magnetization fertig -----")
    return dataframes