from datetime import datetime as dt
import pandas as pd

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
        df.at[index, 'timestamp'] = convert_to_datetime(value)

    return df

def calculate_mean_for_column(df, column):
    try:
        result = df[column].toList().mean()
        return result
    except Exception as e:
        return None
