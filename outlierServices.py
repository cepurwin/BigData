import pandas as pd


def removeOutliersTurkeysMethod_withMean(dataframes, attribute): #Wird eigentlich nur beim timestamp verwendet
    for name, (df, attrs) in dataframes.items():
        # Konvertiere die Timestamps in Unix-Format
        if attribute == 'timestamp':
            df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%dT%H:%M:%S").astype('int64') // 10 ** 9

        Q1 = df[attribute].quantile(0.25)
        Q3 = df[attribute].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Ermitteln der Indizes der Ausreißer
        outliers = df[(df[attribute] < lower_bound) | (df[attribute] > upper_bound)]

        # Berechnen des durchschnittlichen Abstands aller Nicht-Ausreißer-Werte
        non_outliers = df[~df.index.isin(outliers.index)]
        if not non_outliers.empty:
            avg_distance = non_outliers[attribute].diff().abs().mean()
        else:
            avg_distance = 0

        print(f"Ausreißer in {name}:\n")
        for index in outliers.index:
            # Bestimme den bestmöglichen Wert für den Ausreißer basierend auf dem vorherigen Wert (wenn verfügbar)
            if index - 1 in df.index:
                new_value = df.at[index - 1, attribute] + avg_distance
                print(f" - Ersetze Ausreißer an Index {index} ({df.at[index, attribute]}) mit {new_value}")
                df.at[index, attribute] = new_value
            else:
                print(f" - Kann Ausreißer an Index {index} nicht ersetzen, kein Vorgängerwert verfügbar.")

        # Konvertiere die Timestamps wieder in das gewünschte ISO-Format
        if attribute == 'timestamp':
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime("%Y-%m-%dT%H:%M:%S")

    print("Bearbeitung abgeschlossen.\n")
    return dataframes


def removeOutliersTurkeysMethod_withForwardAndBackFill(dataframes, attribute):
    for name, (df, attrs) in dataframes.items():
        Q1 = df[attribute].quantile(0.25)
        Q3 = df[attribute].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Ermitteln der Indizes der Ausreißer
        outliers = df[(df[attribute] < lower_bound) | (df[attribute] > upper_bound)]

        print(f"Ausreißer in {name}:\n")
        for index in outliers.index:
            # Initialisiere die Indizes der neuen Werte
            forward_index = index + 1
            backward_index = index - 1

            # Suche den nächsten gültigen Wert in beide Richtungen
            while forward_index < len(df) and not df.index.isin([forward_index]).any():
                forward_index += 1

            while backward_index >= 0 and not df.index.isin([backward_index]).any():
                backward_index -= 1

            # Überprüfe, ob der Index gültig ist
            if 0 <= backward_index < len(df) and 0 <= forward_index < len(df):
                # Bestimme den nächstgelegenen gültigen Wert
                forward_distance = forward_index - index
                backward_distance = index - backward_index

                if forward_distance <= backward_distance:
                    new_index = forward_index
                else:
                    new_index = backward_index

                # Neuen Wert setzen
                new_value = df.loc[new_index, attribute]
                print(f" - Ersetze Ausreißer an Index {index} ({df.loc[index, attribute]}) mit {new_value}")
                df.at[index, attribute] = new_value
            else:
                print(f" - Index {index} nicht gültig, kann Ausreißer nicht ersetzen.")

    print("Bearbeitung abgeschlossen.\n")
    return dataframes
