# constants for overall API configuration
org = 'H493f0c3e5bf84239'
token = "giJmgHGcBaEt8LvH1kZbfpwrNU3_eYDg32MXqbfkZNyuJHxfyOHTFAyYBsOs7M2s-WKRneuGu849FTT3CNdCHg=="
url="https://westeurope-1.azure.cloud2.influxdata.com/"

# constants dict for specific buckets
bucket_code_test5 = "8bfb0bbb9e31d01a"
bucket_code_test6 = "43ecbfaf3070c072"

# functions for easier access to the constants
def get_client():
    from influxdb_client import InfluxDBClient
    return InfluxDBClient(url=url, token=token, org=org)

def get_query_api():
    return get_client().query_api()

def get_write_api():
    from influxdb_client.client.write_api import SYNCHRONOUS
    return get_client().write_api(write_options=SYNCHRONOUS)