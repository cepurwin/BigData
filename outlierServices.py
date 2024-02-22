import pandas as pd


def removeOutliersTurkeysMethod_withMean(dataframes, attribute):
    for name, (df, attrs) in dataframes.items():
        # Konvertiere die Timestamps in Unix-Format
        if attribute == 'timestamp':
            df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%dT%H:%M:%S").astype(int) // 10 ** 9

        try:
            Q1 = df[attribute].quantile(0.25)
        except Exception as e:
            # Falls ein Fehler auftritt, handele den Fehler
            print(f"Fehler beim Berechnen des 25%-Quantils für '{attribute}': {e}")

            # Extrahiere die nicht-numerischen Werte
            non_numeric_rows = df[pd.to_numeric(df[attribute], errors='coerce').isna()]

            # Gib die nicht-numerischen Werte aus
            print(f"Nicht-numerische Werte für '{attribute}':")
            print(non_numeric_rows)
            print(name)
        Q3 = df[attribute].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Ermitteln der Indizes der Ausreißer
        outliers = df[(df[attribute] < lower_bound) | (df[attribute] > upper_bound)]

        print(f"Ausreißer in {name}:\n")
        for index in outliers.index:
            # Für jeden Ausreißer den Mittelwert der umliegenden Werte berechnen (wenn möglich)
            neighbors = [index - 1, index + 1]

            # Nur gültige Nachbarindizes berücksichtigen
            valid_neighbors = [n for n in neighbors if n in df.index]

            # Berechnen des neuen Werts nur, wenn es gültige Nachbarn gibt
            if valid_neighbors:
                new_value = df.loc[valid_neighbors, attribute].mean()
                print(f" - Ersetze Ausreißer an Index {index} ({df.loc[index, attribute]}) mit {new_value}")
                df.at[index, attribute] = new_value
            else:
                print(f" - Kann Ausreißer an Index {index} nicht ersetzen, keine Nachbarn.")

        # Konvertiere die Timestamps wieder in das gewünschte ISO-Format
        if attribute == 'timestamp':
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime("%Y-%m-%dT%H:%M:%S")

    print("Bearbeitung abgeschlossen.\n")
    return dataframes

def removeOutliersTurkeysMethod_withForwardAndBackFill(dataframes, attribute):
    for name, (df, attrs) in dataframes.items():

        try:
            Q1 = df[attribute].quantile(0.25)
        except Exception as e:
            # Falls ein Fehler auftritt, handele den Fehler
            print(f"Fehler beim Berechnen des 25%-Quantils für '{attribute}': {e}")

            # Extrahiere die nicht-numerischen Werte
            non_numeric_rows = df[pd.to_numeric(df[attribute], errors='coerce').isna()]

            # Gib die nicht-numerischen Werte aus
            print(f"Nicht-numerische Werte für '{attribute}':")
            print(non_numeric_rows)
            print(name)
        Q3 = df[attribute].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Ermitteln der Indizes der Ausreißer
        outliers = df[(df[attribute] < lower_bound) | (df[attribute] > upper_bound)]

        print(f"Ausreißer in {name}:\n")
        for index in outliers.index:
            # Für jeden Ausreißer den Mittelwert der umliegenden Werte berechnen (wenn möglich)
            neighbors = [index - 1, index + 1]

            # Nur gültige Nachbarindizes berücksichtigen
            valid_neighbors = [n for n in neighbors if n in df.index]

            # Berechnen des neuen Werts nur, wenn es gültige Nachbarn gibt
            if valid_neighbors:
                new_value = df.loc[valid_neighbors, attribute].mean()
                print(f" - Ersetze Ausreißer an Index {index} ({df.loc[index, attribute]}) mit {new_value}")
                df.at[index, attribute] = new_value
            else:
                print(f" - Kann Ausreißer an Index {index} nicht ersetzen, keine Nachbarn.")

    print("Bearbeitung abgeschlossen.\n")
    return dataframes
