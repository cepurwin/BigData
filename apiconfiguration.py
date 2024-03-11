# constants for overall API configuration
org = '6102c39593af1a7a'
token = "Idg_OEW4AAssgh_YUaQMETzVTbafiUPT-lurRjx2Qf2reTO8mHU_xJYSi_3vOGLSMAjbuEfuv4FN-4OSrpBY2w=="
url="https://us-central1-1.gcp.cloud2.influxdata.com"

# functions for easier access to the constants
def get_client():
    from influxdb_client import InfluxDBClient
    return InfluxDBClient(url=url, token=token, org=org)

def get_query_api():
    return get_client().query_api()

def get_write_api():
    from influxdb_client.client.write_api import SYNCHRONOUS
    return get_client().write_api(write_options=SYNCHRONOUS)