import argparse
import json
import folium
import folium.plugins as plugins

from datetime import datetime
from pymongo import MongoClient, GEOSPHERE, UpdateOne

def main():
    parser = argparse.ArgumentParser(description="A script for uploding data to MongoDB")

    parser.add_argument("--file", "-f", type=str, help="name of the JSON file to be uploaded")
    parser.add_argument("--url", "-u", type=str, default="mongo.bakajstep.cz", help="hostname of MongoDB server")
    parser.add_argument("--port", "-p", type=int, default="27017", help="port of MongoDB server")
    parser.add_argument("--id", "-i", type=str, default="admin", help="user id")
    parser.add_argument("--password", "-s", type=str, default="admin321", help="password")
    parser.add_argument("--database", "-d", type=str, default="test", help="database name")
    parser.add_argument("--collection", "-c", type=str, default="test", help="collection of database")
    parser.add_argument("--action", "-a", type=str, default="store", help="action to do with database (store or load)")
    parser.add_argument("--latitude", "-w", type=float, default=49.22655516496612, help="latitude coordinate")
    parser.add_argument("--longitude", "-l", type=float, default=16.595914968837057, help="longitude coordinate")

    args = parser.parse_args()

    try:
        FILE = args.file
        URL = args.url
        PORT = args.port
        ID = args.id
        PASSWORD = args.password
        DATABASE = args.database
        COLLECTION = args.collection
        ACTION = args.action
        LATITUDE = args.latitude
        LONGITUDE = args.longitude
    except ValueError:
        print("Invalid arguments format.")

    client = MongoClient("mongodb://"+ID+":"+PASSWORD+"@"+URL+":"+str(PORT))
    db = client[DATABASE]
    collection = db[COLLECTION]

    try:
        db.command("serverStatus")
    except Exception as e:
        print(e)
    else:
        print("Connected to MongoDB server!")

    if (ACTION == "store"):
        if FILE is None:
            raise Exception("Missing input file")
        else:
            storeData(FILE, collection)
    elif (ACTION == "load"):
        loadData(collection, LATITUDE, LONGITUDE)
    else:
        raise Exception("Wrong action parameter")

    try:
        client.close()
    except Exception as e:
        print("Unable to disconnect from server!")
        print(e)
    else:
        print("Connection successfully closed!")


def storeData(FILE, collection):
    with open(FILE, "r") as json_file:
        data = json.load(json_file)
    
    try:
        updates = []
        for feature in data["features"]:
            properties = feature["properties"]
            properties["location"] = feature["geometry"]
            _id = int(properties["ID"])
            feature["_id"] = _id
            updates.append(UpdateOne({"_id": _id}, {"$set": properties}, upsert=True))
            
        collection.bulk_write(updates)
        collection.create_index([("location", GEOSPHERE)])
    except Exception as e:
        print("Unable to store data to database!")
        print(e)
    else:
        print("Data successfuly stored to server.")


def loadData(collection, latitude: float, longitude: float):
    nearby_events = get_nearby_events(collection, latitude, longitude)
    display_events_on_map(nearby_events, latitude, longitude)


def get_nearby_events(collection, latitude: float, longitude: float):
    nearby_events = collection.find({
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$maxDistance": 500
            }
        }
    })

    return nearby_events


def display_events_on_map(events, default_latitude: float, default_longitude: float):
    m = folium.Map(location=[default_latitude, default_longitude])
    marker_cluster = plugins.MarkerCluster().add_to(m)

    folium.Marker(
        [default_latitude, default_longitude],
        tooltip="Zadaná poloha",
        icon=folium.Icon(icon="user", prefix="fa", color="red"),
    ).add_to(m)

    all_coords = []
    
    for event in events:
        longitude, latitude = event["location"]["coordinates"]
        name = event["name"]
        url = event["url"]
        date_from = event["date_from"]
        date_to = event["date_to"]

        date_from_czech = datetime.strptime(date_from, "%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y")
        date_to_czech = datetime.strptime(date_to, "%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y")

        all_coords.append([latitude, longitude])

        marker = folium.Marker([latitude, longitude], tooltip=name)
        shown_data = f"<strong>{name}</strong><br>Termín: od&nbsp;{date_from_czech} do&nbsp;{date_to_czech}<br><a href='{url}' target='_blank'>Odkaz na akci</a>"
        marker.add_child(folium.Tooltip(shown_data))
        marker.add_child(folium.Popup(shown_data))
        marker.add_to(m)
        marker.add_to(marker_cluster)

    if all_coords:
        m.fit_bounds(all_coords, padding=[10, 10])

    m.save("map.html")
    print("Map saved as map.html")


if __name__ == "__main__":
    main()
