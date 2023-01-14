from datetime import datetime
import os

import cfg_load
config_db = cfg_load.load("credential.yaml")
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = config_db["token"]
org = "frederik.andre.savard@gmail.com"
bucket = "frederik.andre.savard's Bucket"

with InfluxDBClient(url="https://us-central1-1.gcp.cloud2.influxdata.com", token=token, org=org) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)

    data = "mem,host=host1 used_percent=23.43234543"
    write_api.write(bucket, org, data)
    client.close()


