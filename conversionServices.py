from datetime import datetime
import pandas as pd


def get_datetime_from_unix_timestamp(ts):
    dt = datetime.fromtimestamp(ts, tz=None)
    return dt


def is_valid_unix_timestamp(ts):
    if get_datetime_from_unix_timestamp(ts):
        return True
    else:
        return False

def convert_timestamp_iso_to_unix(timestamp):
    timestamp_str = str(timestamp)
    if 'T' in timestamp_str:
        timestamp_str_padded = timestamp_str[:-1] + "0" + timestamp_str[-1] if timestamp_str[-2] == ':' else timestamp_str
        timestamp_dt = datetime.strptime(timestamp_str_padded, '%Y-%m-%dT%H:%M:%S')
        return timestamp_dt.timestamp()
    else:
        return timestamp

def convert_bytestring_to_unicode_cell(cell_value):
    decoded_str = cell_value.decode('utf-8')
    try:
        new_value = float(decoded_str)
    except ValueError:
        new_value = cell_value.decode('utf-8')
    return new_value

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