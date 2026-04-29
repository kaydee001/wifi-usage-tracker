import csv
import time
import psutil
import datetime
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(figsize=(10, 5))
time_data, upload_data, download_data = [], [], []

ax.grid(True)

plt.tight_layout()

previous_counters = psutil.net_io_counters()


def calculate_speed(old_counters, new_counters):
    upload_speed = (new_counters.bytes_sent - old_counters.bytes_sent)/1024
    download_speed = (new_counters.bytes_recv - old_counters.bytes_recv)/1024

    return upload_speed, download_speed


def update(current_frame):
    global previous_counters
    current_counters = psutil.net_io_counters()

    upload_speed = (current_counters.bytes_sent -
                    previous_counters.bytes_sent) / 1024
    download_speed = (current_counters.bytes_recv -
                      previous_counters.bytes_recv) / 1024

    upload_data.append(upload_speed)
    download_data.append(download_speed)
    time_data.append(current_frame)

    upload_line.set_data(time_data, upload_data)
    download_line.set_data(time_data, download_data)

    previous_counters = current_counters

    max_speed = max(max(upload_data, default=100),
                    max(download_data, default=100))

    ax.set_xlim(0, current_frame + 1)
    ax.set_ylim(0, max_speed*1.2)

    return upload_line, download_line


upload_line, = ax.plot([], [], "r-", label="upload KB/s")
download_line, = ax.plot([], [], "b-", label="download KB/s")

ax.legend()

ani = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)


def track_speed():
    previous_counters = psutil.net_io_counters()

    header = ["upload_speed", "download_speed", "time"]

    with open("output.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)

    while True:
        current_time = datetime.datetime.now()

        current_counters = psutil.net_io_counters()

        upload_speed, download_speed = calculate_speed(
            previous_counters, current_counters)

        print(
            f"upload : {upload_speed:.2f} KB/s | download : {download_speed:.2f} KB/s")

        with open("output.csv", "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([upload_speed, download_speed, current_time])

        previous_counters = current_counters

        time.sleep(1)


if __name__ == "__main__":
    track_theard = threading.Thread(target=track_speed, daemon=True)

    track_theard.start()
    plt.show()
