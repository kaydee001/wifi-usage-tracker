import csv
import time
import psutil
import datetime
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
time_data, upload_data, download_data = [], [], []

upload_line, = plt.plot([], [], "r-", label="upload KB/s")
download_line, = plt.plot([], [], "b-", label="download KB/s")

ax.legend()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

old = psutil.net_io_counters()


def update(frame):
    global old
    new = psutil.net_io_counters()

    upload_speed = (new.bytes_sent - old.bytes_sent) / 1024
    download_speed = (new.bytes_recv - old.bytes_recv) / 1024

    upload_data.append(upload_speed)
    download_data.append(download_speed)
    time_data.append(frame)

    upload_line.set_data(time_data, upload_data)
    download_line.set_data(time_data, download_data)

    old = new

    return upload_line, download_line


ani = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
# plt.show()


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
            f"upload : {upload_speed:.2f} KB/s | download : {download_speed:.2f} KB/s")

        with open("output.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow([upload_speed, download_speed, timestamp])

        old_bytes_sent = new_bytes_sent
        old_bytes_received = new_bytes_received

        time.sleep(1)


if __name__ == "__main__":
    track_theard = threading.Thread(target=track_speed, daemon=True)

    track_theard.start()
    plt.show()
