import argparse
import csv

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datetime import datetime, timezone
from dateutil import parser


def main():
    parserARG = argparse.ArgumentParser(description="A script for uploding data to Cassandra")

    parserARG.add_argument("--file", "-f", type=str, required=True, help="name of the CSV file to be uploaded")
    parserARG.add_argument("--port", "-p", type=int, help="port", default="9042")
    parserARG.add_argument("--url", "-u", type=str, default="192.168.1.8",
                        help="hostname or IP of Cassandra server")
    parserARG.add_argument("--keyspace", "-k", type=str, default="brno_jams", help="name of keyspace")

    args = parserARG.parse_args()
    auth_provider = PlainTextAuthProvider(username='admin', password='admin321')

    # cluster = Cluster([args.url], port=args.port, auth_provider=auth_provider)
    cluster = Cluster(['192.168.1.8'], port=9042, auth_provider=auth_provider)
    session = cluster.connect()

    # Check if the keyspace exists
    keyspace_name = args.keyspace
    keyspace_query = "SELECT * FROM system_schema.keyspaces WHERE keyspace_name = %s"
    keyspace_exists = session.execute(keyspace_query, [keyspace_name])

    # Create the keyspace if it doesn't exist
    if not keyspace_exists:
        create_keyspace_query = f"""
        CREATE KEYSPACE {keyspace_name}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}};
        """
        session.execute(create_keyspace_query)

    session.set_keyspace(keyspace_name)

    create_table_query = """
    CREATE TABLE IF NOT EXISTS brno_jam (
        country text,
        level int,
        city text,
        speed_KMH int,
        length int,
        uuid int,
        end_node text,
        speed_MS int,
        blocking_Alert_Uuid text,
        road_Type text,
        delay int,
        street text,
        pub_Millis timestamp,
        PRIMARY KEY (level, uuid)
    );
    """

    session.execute(create_table_query)

    with open(args.file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if needed
        for row in reader:
            date_string = row[16].split('+')[0].strip()
            date_object = parser.parse(date_string)
            # Convert the date object to UTC and extract the components
            date_object_utc = date_object.astimezone(timezone.utc)
            insert_query = session.prepare("INSERT INTO brno_jam (country, level, city, speed_KMH, length, uuid, end_node, speed_MS, blocking_Alert_Uuid, road_Type, delay, street, pub_Millis) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);")
            session.execute(insert_query, (row[0], int(row[1]), row[2], int(row[3]), int(row[4]), int(row[8]), row[9], int(row[10]), row[11], row[12], int(row[13]), row[14], date_object_utc))

    # Close the connection to the Cassandra cluster
    cluster.shutdown()


if __name__ == "__main__":
    main()