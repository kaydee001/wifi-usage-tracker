import csv
import time
import psutil
import datetime
import threading
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import MaxNLocator

MAX_VISIBLE_POINTS = 60
SMOOTHING_WINDOW = 5

fig, (upload_ax, download_ax) = plt.subplots(
    2, 1, figsize=(10, 6), sharex=True)
time_data, upload_data, download_data = [], [], []

upload_ax.set_title("upload speed")
download_ax.set_xlabel("time")
upload_ax.set_ylabel("Mbps")
upload_ax.grid(True)

download_ax.set_title("download speed")
download_ax.set_xlabel("time")
download_ax.set_ylabel("Mbps")
download_ax.grid(True)

plt.tight_layout()

previous_counters = psutil.net_io_counters()


def calculate_speed(old_counters, new_counters):
    upload_speed = (
        (new_counters.bytes_sent - old_counters.bytes_sent) * 8
    ) / (1024 * 1024)

    download_speed = (
        (new_counters.bytes_recv - old_counters.bytes_recv) * 8
    ) / (1024 * 1024)

    return upload_speed, download_speed


def moving_average(data, SMOOTHING_WINDOW):
    weights = np.ones(SMOOTHING_WINDOW)/SMOOTHING_WINDOW
    return np.convolve(data, weights, mode="valid")


def update(current_frame):
    global previous_counters

    current_counters = psutil.net_io_counters()

    upload_speed, download_speed = calculate_speed(
        previous_counters, current_counters)

    upload_data.append(upload_speed)
    download_data.append(download_speed)
    time_data.append(current_frame)
    previous_counters = current_counters

    if len(upload_data) < 5:
        return upload_line, download_line

    smoothed_upload = moving_average(
        upload_data[-MAX_VISIBLE_POINTS:], SMOOTHING_WINDOW)
    smoothed_download = moving_average(
        download_data[-MAX_VISIBLE_POINTS:], SMOOTHING_WINDOW)

    upload_line.set_data(time_data[-len(smoothed_upload):], smoothed_upload)
    download_line.set_data(
        time_data[-len(smoothed_download):], smoothed_download)

    visible_upload = upload_data[-MAX_VISIBLE_POINTS:]
    visible_download = download_data[-MAX_VISIBLE_POINTS:]

    upload_max = max(visible_upload, default=100)
    download_max = max(visible_download, default=100)

    upload_ax.set_xlim(
        max(0, current_frame-MAX_VISIBLE_POINTS), current_frame+1)
    upload_ax.set_ylim(0, max(upload_max * 1.2, 5))

    upload_ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    download_ax.set_xlim(
        max(0, current_frame-MAX_VISIBLE_POINTS), current_frame+1)
    download_ax.set_ylim(0, max(download_max * 1.2, 100))

    download_ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    return upload_line, download_line


upload_line, = upload_ax.plot([], [], "r-", label="upload Mbps")
upload_ax.legend()

download_line, = download_ax.plot([], [], "b-", label="download Mbps")
download_ax.legend()

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
            f"upload : {upload_speed:.1f} Mbps | download : {download_speed:.1f} Mbps")

        with open("output.csv", "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([upload_speed, download_speed, current_time])

        previous_counters = current_counters

        time.sleep(1)


if __name__ == "__main__":
    track_thread = threading.Thread(target=track_speed, daemon=True)

    track_thread.start()
    plt.show()
