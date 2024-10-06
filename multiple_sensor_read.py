import csv
import datetime
import umyo_parser
from collections import deque
import copy
import numpy as np
import time

buffer_size = 500
full_data_stream = deque(maxlen=buffer_size)
filename = 'csv_data.csv'
num_of_devices = 3
last_data_id = []
data_spg = []
ordered_data_stream = [[0] * 4] * num_of_devices
counter = [0] * num_of_devices


# initializes the data lists based on the number of devices


def init():
    global last_data_id, data_spg, num_of_devices
    for i in range(num_of_devices):
        data_spg.append([0] * 5)
        last_data_id.append([0])


def handle_data(devices):
    global data_spg, last_data_id
    cnt = len(devices)
    if cnt < 1: return
    for d in range(cnt):
        # updates data_spg[d] with the latest processed EMG data
        # when packet id is different
        if devices[d].data_id != last_data_id[d]:
            for n in range(4):
                data_spg[d].append(devices[d].device_spectr[n])
            data_spg[d] = data_spg[d][-4:]
        else:
            data_spg[d] = [0]*5
        last_data_id[d] = devices[d].data_id


def save_data_to_csv(data_deque, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_write = csv.writer(csvfile)
        for row in data_deque:
            flattened_row = [item for sublist in row for item in sublist]
            csv_write.writerow(flattened_row)
        data_deque.clear()


# list
from serial.tools import list_ports

port = list(list_ports.comports())
print("available ports:")
for p in port:
    print(p.device)
    device = p.device
print("===")

# read
import serial

ser = serial.Serial(port=device, baudrate=921600, parity=serial.PARITY_NONE, stopbits=1, bytesize=8, timeout=0)

print("conn: " + ser.portstr)

# main loop

init()  # Initialize the lists

try:
    while (1):
        # collecting data from sensors
        cnt = ser.in_waiting
        if (cnt > 0):
            # data = data packet from any sensor
            data = ser.read(cnt)
            # data is read from device, processed, and saved into:
            # umyo_parser.umyo_get_list
            umyo_parser.umyo_parse_preprocessor(data)
            # handle_data checks from which sensor the packet was received from,
            # and saves the data.
            handle_data(umyo_parser.umyo_get_list())
            for index, data_list in enumerate(data_spg):
                if len(data_list) < 5:
                    ordered_data_stream[index] = data_list
                    counter[index] = 1
            if sum(counter) < num_of_devices:
                continue  # continue getting packets until values from all sensors are obtained
            else:
                counter = [0] * num_of_devices
                timestamp = int(time.time() * 1000)
                time_list = [timestamp]
                ordered_data_stream.append(time_list)
                full_data_stream.append(copy.deepcopy(ordered_data_stream))
                ordered_data_stream = [[0] * 4] * num_of_devices
                if len(full_data_stream) >= buffer_size:
                    save_data_to_csv(full_data_stream, filename)
except KeyboardInterrupt:
    # Handle graceful shutdown on user interruption (Ctrl+C)
    print("Data stream interrupted by user. Saving remaining data...")
    if full_data_stream:
        save_data_to_csv(full_data_stream, filename)
