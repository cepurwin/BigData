def filterEasterEggs(dataframes):
    for name, (df, attrs) in dataframes.items():
        condition = df.map(lambda cell: isinstance(cell, bytes) and cell == b'Easteregg :)' or isinstance(cell, str) and cell == 'Easteregg :)')
        rows_to_drop = condition.any(axis=1)

        df.drop(df[rows_to_drop].index, inplace=True)
    return dataframes

def replace_nan_with_avg_of_neighbors(dataframes, attribute):
    for name, (df, attrs) in dataframes.items():
        print(f"Bearbeite {name}...")

        # Vorwärts füllen (nutzt nächstfolgenden gültigen Wert)
        forward_filled = df[attribute].fillna(method='ffill')

        # Rückwärts füllen (nutzt vorherigen gültigen Wert)
        backward_filled = df[attribute].fillna(method='bfill')

        # Durchschnitt zwischen vorwärts und rückwärts gefüllten Werten nehmen
        averaged = (forward_filled + backward_filled) / 2

        # Behandlung von Fällen, bei denen entweder am Anfang oder am Ende NaN-Werte stehen.
        # Wenn averaged noch NaN-Werte enthält, bedeutet dies, dass sowohl forward als auch backward fill nicht funktioniert haben.
        # In diesem Fall wird NaN durch den gültigen Wert von forward_filled oder backward_filled ersetzt.
        # Da beide in jedem Fall den gleichen Wert haben sollten (wenn einer von ihnen NaN ist, ist der andere nicht),
        # kann jeder von ihnen verwendet werden, um die verbleibende NaN zu ersetzen.
        df[attribute] = averaged.fillna(forward_filled)

    print("Bearbeitung abgeschlossen.\n")
    return dataframes
