import psutil
import time
import datetime
import csv


def track_speed():
    old_bytes_sent = psutil.net_io_counters().bytes_sent
    old_bytes_received = psutil.net_io_counters().bytes_recv

    time.sleep(1)

    header = ["upload_speed", "download_speed", "time"]

    with open("output.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(header)

    while True:
        timestamp = datetime.datetime.now()

        new_bytes_sent = psutil.net_io_counters().bytes_sent
        new_bytes_received = psutil.net_io_counters().bytes_recv

        upload_speed = (new_bytes_sent-old_bytes_sent)/1024
        download_speed = (new_bytes_received-old_bytes_received)/1024

        print(
            f"upload speed : {upload_speed:.2f} KB/s")
        print(
            f"download speed : {download_speed:.2f} KB/s")

        with open("output.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow([upload_speed, download_speed, timestamp])

        old_bytes_sent = new_bytes_sent
        old_bytes_received = new_bytes_received

        time.sleep(1)


if __name__ == "__main__":
    track_speed()
