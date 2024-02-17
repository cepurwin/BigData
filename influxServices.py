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
                 .tag("cofiguration", attrs["configuration"])
                 .tag("year", year)
                 .tag("avg_velocity", avg_velo)
                 .field("defect_channel", row[1]["defect_channel"])
                 .field("distance", row[1]["distance"])
                 .field("magnetization", row[1]["magnetization"])
                 .field("velocity", row[1]["velocity"])
                 .field("wall_thickness", row[1]["wall_thickness"]))

            points.append(p)

        api.get_write_api().write(bucket=bucket, org=api.org, record=points)