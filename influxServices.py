import conversionServices as convServ
import apiconfiguration as api
import influxdb_client as influx
def upload_dict_with_frames(dict, bucket):
    for name, (frame, attrs) in dict.items():

        year = convServ.getYearFromDf(frame) # extract year from timestamp
        avg_velo = convServ.calculate_mean_for_column(dict, "velocity")
        points = []

        for row in frame.iterrows():

            p = (influx.Point(name)
                 .time(row[1]["timestamp"]) # Muss bereits als datetime vorliegen
                 .tag("instrument", attrs["instrument"])
                 .tag("configuration", attrs["configuration"])
                 .tag("year", year)
                 .tag("avg_velocity", avg_velo)
                 .field("defect_channel", row[1]["defect_channel"])
                 .field("distance", row[1]["distance"])
                 .field("magnetization", row[1]["magnetization"])
                 .field("velocity", row[1]["velocity"])
                 .field("wall_thickness", row[1]["wall_thickness"]))

            points.append(p)

        api.get_write_api().write(bucket=bucket, org=api.org, record=points)

def get_measurements_from_bucket(bucket):
    query = (f'from(bucket:"{bucket}")\
    |> range(start: 0)\
    |> keys()')
    result = api.get_query_api().query(org=api.org, query=query)
    measurements = []
    for table in result:
        for record in table.records:
            curr_measurement = record.get_measurement()
            if curr_measurement not in measurements:
                measurements.append(curr_measurement)
            else:
                continue
    return measurements

def download_df_by_measurement(bucket, measurement):
    # Query aufbauen
    query = (f'from(bucket:"{bucket}")\
    |> range(start: 0)\
    |> filter(fn: (r) => r._measurement == "{measurement}")\
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")')

    # Query ausführen
    df = api.get_query_api().query_data_frame(org=api.org, query=query)

    # Attribute sind in allen Zeilen gleich, deshalb reicht es, die ersten Zeilen zu betrachten
    attrs = {}
    for row in df.iterrows():
        attrs['instrument'] = row[1]['instrument']
        attrs['configuration'] = row[1]['cofiguration']
        attrs['year'] = row[1]['year']
        break

    #Spalte "_time" in "timestamp" umbenennen
    df = df.rename(columns={"_time": "timestamp"})

    #Attribut-Spalten löschen
    df = df.drop(['_measurement', '_start', '_stop', 'table','result', 'instrument', 'cofiguration', 'year'], axis=1)

    return df, attrs

def download_all_dataframes(bucket):
    measurements = get_measurements_from_bucket("test5")
    dataframes = {}
    for measurement in measurements:
        dataframes[measurement] = download_df_by_measurement("test5", measurement)
    return dataframes
