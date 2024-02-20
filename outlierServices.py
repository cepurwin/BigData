import pandas as pd


def removeOutliersTurkeysMethod(dataframes):
    for name, (df, attrs) in dataframes.items():
        # Wir gehen davon aus, dass 'timestamp' der Name der Spalte ist, die geprüft werden soll
        df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
        Q1 = df['timestamp'].quantile(0.25)
        Q3 = df['timestamp'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Ermitteln der Indizes der Ausreißer
        outliers = df[(df['timestamp'] < lower_bound) | (df['timestamp'] > upper_bound)]

        print(f"Ausreißer in {name}:\n")
        for index in outliers.index:
            # Für jeden Ausreißer den Mittelwert der umliegenden Werte berechnen (wenn möglich)
            neighbors = [index - 1, index + 1]

            # Nur gültige Nachbarindizes berücksichtigen
            valid_neighbors = [n for n in neighbors if n in df.index]

            # Berechnen des neuen Werts nur, wenn es gültige Nachbarn gibt
            if valid_neighbors:
                new_value = df.loc[valid_neighbors, 'timestamp'].mean()
                print(f" - Ersetze Ausreißer an Index {index} ({df.loc[index, 'timestamp']}) mit {new_value}")
                df.at[index, 'timestamp'] = new_value
            else:
                print(f" - Kann Ausreißer an Index {index} nicht ersetzen, keine Nachbarn.")
    print("Bearbeitung abgeschlossen.\n")
