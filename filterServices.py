import pandas as pd

def filterEasterEggs(dataframes):
    for name, (df, attrs) in dataframes.items():
        condition = df.map(lambda cell: isinstance(cell, bytes) and cell == b'Easteregg :)' or isinstance(cell, str) and cell == 'Easteregg :)')
        rows_to_drop = condition.any(axis=1)

        df.drop(df[rows_to_drop].index, inplace=True)
    return dataframes

def convert_all_strings_to_floats(dataframes_dict):
    for name, (df, attrs) in dataframes_dict.items():
        # Überprüfe 'magnetization' und 'wall_thickness' auf Strings und konvertiere sie zu Floats
        for col in ['magnetization', 'wall_thickness']:
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
                except ValueError as ve:
                    print(f"Error converting {col} to float in DataFrame '{name}': {ve}")
                    non_numeric_values = df[df[col].apply(lambda x: not str(x).replace('.', '', 1).isdigit())][col]
                    print(f"Non-numeric values in '{col}':\n{non_numeric_values}")

    return dataframes_dict


def replace_nan_with_avg_of_neighbors(dataframes, attribute):
    for name, (df, attrs) in dataframes.items():
        print(f"Bearbeite {name}...")

        # Vorwärts füllen (nutzt nächstfolgenden gültigen Wert)
        forward_filled = df[attribute].fillna(method='ffill')

        # Rückwärts füllen (nutzt vorherigen gültigen Wert)
        backward_filled = df[attribute].fillna(method='bfill')

        # Durchschnitt zwischen vorwärts und rückwärts gefüllten Werten nehmen
        df[attribute] = (forward_filled + backward_filled) / 2

    print("Bearbeitung abgeschlossen.\n")
    return dataframes
