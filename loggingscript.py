from datetime import datetime
import os
import time
from google.transit import gtfs_realtime_pb2
import pandas as pd
import requests

# 511 SF Bay API Settings
API_KEY = "YOUR_511_API_KEY_HERE"
AGENCY = "AC"
ROUTE_TARGET = "51A"
ENDPOINT_URL = f"https://api.511.org/transit/TripUpdates?api_key={API_KEY}&agency={AGENCY}"

CSV_FILENAME = "master_broadway_delays.csv"
POLL_INTERVAL_SECONDS = 300  # Poll every 5 minutes


def fetch_and_log_gtfs():
    """Fetches real-time GTFS-RT predictions from 511.org and appends to CSV."""
    poll_time = datetime.now()

    try:
        # 511.org returns protobuf binary feed
        response = requests.get(
            ENDPOINT_URL, headers={"Accept-Encoding": "gzip"}, timeout=15
        )
        response.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        records = []

        for entity in feed.entity:
            if entity.HasField("trip_update"):
                trip_update = entity.trip_update
                route_id = trip_update.trip.route_id

                # Filter strictly for Line 51A
                if route_id == ROUTE_TARGET:
                    trip_id = trip_update.trip.trip_id

                    for stu in trip_update.stop_time_update:
                        stop_id = stu.stop_id

                        # Extract arrival timestamp (POSIX timestamp)
                        if stu.HasField("arrival") and stu.arrival.time:
                            arrival_timestamp = pd.to_datetime(
                                stu.arrival.time, unit="s"
                            )
                        elif stu.HasField("departure") and stu.departure.time:
                            arrival_timestamp = pd.to_datetime(
                                stu.departure.time, unit="s"
                            )
                        else:
                            continue

                        records.append(
                            {
                                "poll_timestamp": poll_time,
                                "trip_id": trip_id,
                                "route_id": route_id,
                                "stop_id": stop_id,
                                "arrival_time": arrival_timestamp,
                            }
                        )

        if records:
            df_new = pd.DataFrame(records)

            # Check if CSV exists to handle headers
            file_exists = os.path.isfile(CSV_FILENAME)
            df_new.to_csv(
                CSV_FILENAME, mode="a", header=not file_exists, index=False
            )

            print(
                f"[{poll_time.strftime('%Y-%m-%d %H:%M:%S')}] Logged {len(records)} 51A arrival predictions to {CSV_FILENAME}."
            )
        else:
            print(
                f"[{poll_time.strftime('%Y-%m-%d %H:%M:%S')}] Active feed returned no updates for Line 51A."
            )

    except Exception as e:
        print(f"[{poll_time.strftime('%Y-%m-%d %H:%M:%S')}] Error: {e}")


if __name__ == "__main__":
    print(
        f"Starting GTFS Logger for AC Transit Line {ROUTE_TARGET} via 511 SF Bay API..."
    )
    print(f"Saving to: {CSV_FILENAME} every {POLL_INTERVAL_SECONDS} seconds.\n")

    while True:
        fetch_and_log_gtfs()
        time.sleep(POLL_INTERVAL_SECONDS)