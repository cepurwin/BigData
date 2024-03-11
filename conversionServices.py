from datetime import datetime as dt
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def convert_to_datetime(timestamp):
    # Annahme: Timestamp ist entweder ein String oder ein Unix-Timestamp
    # Annahme: Bytestrings wurden bereits in Unicode umgewandelt
    format_iso = "%Y-%m-%dT%H:%M:%S"
    try:
        val = float(timestamp)
    except Exception as e:
        val = timestamp

    if isinstance(val, str):
        return dt.strptime(val, format_iso)
    elif isinstance(val, float):
        return dt.fromtimestamp(val)
    else:
        # Bei Fehler wird Jahr 2100 zurückgegeben
        # Kein Error-Handling, da dies bei der Ausreißer-Erkennung auffallen sollte
        return dt.strptime("2100-01-01T00:00:00", format_iso)

def getYearFromDf(dataframe):
    if not None:
        timestamp = dataframe['timestamp'].iloc[0]

        try:
            datetime_obj = pd.to_datetime(timestamp, unit='s', utc=True)
            year = datetime_obj.year
        except (ValueError, TypeError):
            try:
                year = int(str(timestamp)[:4])
            except Exception as e:
                print(f"Fehler bei der Jahr-Extraktion: {e}")
                year = None
                return 0

        return year

def convert_for_influx(df):
    # Für alle Spalten durchlaufen
    for column in df.keys().tolist():
        df[column] = df[column].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

    # Nur für timestamp durchlaufen
    for index, value in enumerate(df['timestamp']):
        try:
            df.at[index, 'timestamp'] = convert_to_datetime(value)
        except Exception as e:
            print(e)

    return df

def calculate_mean_for_column(df, column):
    try:
        result = df[column].toList().mean()
        return result
    except Exception as e:
        return None

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

def calculate_velocity_conditionally(dataframes):
    """Berechnet fehlende 'velocity' Werte nur unter bestimmten Bedingungen für jedes DataFrame im gegebenen Dict.

    Die Bedingungen sind:
    - Es gibt Null-Werte in 'velocity', oder
    - Die Anzahl der Datensätze ist weniger als 1000
    Für den ersten Datensatz wird 'velocity' auf 0 gesetzt, wenn keine Berechnung möglich ist.

    Parameter:
        dataframes (dict): Dictionary von DataFrames.
    """
    for name, (df, attrs) in dataframes.items():
        # Prüfe Bedingungen: Existenz von NaN in 'velocity' oder weniger als 1000 Datensätze
        if df['velocity'].isnull().any() or len(df) < 1000:
            print(f"Bedingungen erfüllt, berechne 'velocity' für {name}.")

            # Konvertiere timestamp von datetime zu UNIX
            df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%dT%H:%M:%S").astype('int64') // 10 ** 9

            # Berechnung des Zeitunterschieds
            df['time_diff'] = df['timestamp'].diff()

            # Angenommen 'distance' existiert bereits, berechne 'velocity'
            df['velocity'] = df['distance'] / df['time_diff']

            # Behandeln von Fällen mit Zeitdifferenz von 0 und setze den ersten 'velocity' Wert auf 0, falls erforderlich
            df.loc[df['time_diff'] == 0, 'velocity'] = np.NaN

            # Um die Warnung zu vermeiden, verwenden wir .loc mit dem expliziten Index des ersten Datensatzes
            first_index = df.index[0]
            df.loc[first_index, 'velocity'] = 0

            # Entferne die 'time_diff' Spalte
            df.drop('time_diff', axis=1, inplace=True)

            # Konvertiere timestamp zurück zu datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime("%Y-%m-%dT%H:%M:%S")

            # Update das DataFrame im originalen Dictionary
            dataframes[name] = (df, attrs)
        else:
            print(f"'velocity' Werte bereits vorhanden und mehr als 1000 Datensätze in {name}, überspringe die Berechnung.")

    return dataframes