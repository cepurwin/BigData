from datetime import datetime as dt
import pandas as pd


def get_datetime_from_unix_timestamp(ts):
    datet = dt.fromtimestamp(ts, tz=None)
    return datet


def is_valid_unix_timestamp(ts):
    if get_datetime_from_unix_timestamp(ts):
        return True
    else:
        return False

def convert_timestamp_iso_to_unix(timestamp):
    timestamp_str = str(timestamp)
    if 'T' in timestamp_str:
        timestamp_str_padded = timestamp_str[:-1] + "0" + timestamp_str[-1] if timestamp_str[-2] == ':' else timestamp_str
        timestamp_dt = dt.strptime(timestamp_str_padded, '%Y-%m-%dT%H:%M:%S')
        return timestamp_dt.timestamp()
    else:
        return timestamp

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

def convert_bytestring_to_unicode(value):
    return value.decode('utf-8')

def try_convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return value

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

def dataframe_column_average(df, column_name):
    return df[column_name].mean()

def convert_for_influx(df):
    columns = df.keys().tolist()
    # columns.remove("timestamp")

    for index, row in df.iterrows():
        # Für alle Spalten außer timestamp durchlaufen
        for column in columns:
            if isinstance(row[column], bytes):
                df.at[index, column] = convert_bytestring_to_unicode(row[column])
            if isinstance(row[column], str):
                df.at[index, column] = try_convert_to_float((row[column]))


    for index, value in enumerate(df['timestamp']):
        # if isinstance(value, float):
        #     df.at[index, 'timestamp'] = pd.to_datetime(value, unit='s')
        # else:
        df.at[index, 'timestamp'] = convert_to_datetime(value)

    return df

