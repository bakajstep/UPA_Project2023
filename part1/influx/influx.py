import argparse
import csv
from influxdb_client import InfluxDBClient, Point, WriteOptions
from datetime import datetime


def parse_row(row):
    point = Point("enviroment-control") \
    .tag('objectid', row[2] if row[2] else None) \
    .tag('code', row[3] if row[3] else None) \
    .tag('name', row[4] if row[4] else None) \
    .tag('owner', row[5] if row[5] else None) \
    .tag('lat', row[6] if row[6] else None) \
    .tag('lon', row[7] if row[7] else None) \
    .time(time=datetime.strptime(row[8], "%Y/%m/%d %H:%M:%S+00"))

    # Conditionally set field values if they are not empty
    if row[9]:
        point.field('so2_1h', float(row[9]))
    if row[10]:
        point.field('no2_1h', float(row[10]))
    if row[11]:
        point.field('co_8h', float(row[11]))
    if row[12]:
        point.field('pm10_1h', float(row[12]))
    if row[13]:
        point.field('o3_1h', float(row[13]))
    if row[14]:
        point.field('pm10_24h', float(row[14]))
    if row[15]:
        point.field('pm2_5_1h', float(row[15])) 
    return point


def main():
    parser = argparse.ArgumentParser(description="A script for uploding data to InfluxDB")
    
    parser.add_argument("--file", "-f", type=str, required=True, help="name of the CSV file to be uploaded")
    parser.add_argument("--url", "-u", type=str, default="https://influx.bakajstep.cz", help="hostname of Influx server")
    parser.add_argument("--token", "-t", type=str, default="u3D1fikApZeEmMIbkY358SDjRsLMbY1rpUNZqjLxAs7NAPh5d7mM2RfHVtHVVYkbOjiWQXtnou9Z-OCC8EkgkA==", help="token for autentication")
    parser.add_argument("--organization", "-o", type=str, default="vut", help="name of organization")
    parser.add_argument("--bucket", "-b", type=str, default="vut", help="name of bucket")

    args = parser.parse_args()
    
    try:
        DB_HOSTNAME=args.url
        TOKEN = args.token
        ORGANIZATION = args.organization
        FILE = args.file
        BUCKET = args.bucket
    except ValueError:
        print("Invalid arguments format.")

    client = InfluxDBClient(url=DB_HOSTNAME, token=TOKEN, org=ORGANIZATION)
    write_api = client.write_api()


    list_of_points = []
    with open(FILE, 'r', encoding="UTF-8") as csv_file:
        csv_reader = csv.reader(csv_file)

        # Skip the header row
        next(csv_reader)
        i = 0
        # Iterate through the rows in the CSV file
        for row in csv_reader:
            list_of_points.append(parse_row(row))
        
    # Write Poit to InfluxDB
    write_api.write(bucket=BUCKET, org=ORGANIZATION, record=list_of_points)
    write_api.close()


if __name__ == "__main__":
    main()
