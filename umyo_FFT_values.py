import csv
import datetime
import display_stuff
import umyo_parser
from collections import deque

buffer_size = 500
full_data_stream = deque(maxlen=buffer_size)
filename = 'csv_data.csv'

def save_data_to_csv(data_deque, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_write = csv.writer(csvfile)
        for row in data_deque:
            csv_write.writerow(row)
        data_deque.clear()
# list
from serial.tools import list_ports
port = list(list_ports.comports())
print("available ports:")
for p in port:
    print(p.device)
    device = p.device
print("===")

#read
import serial
ser = serial.Serial(port=device, baudrate=921600, parity=serial.PARITY_NONE, stopbits=1, bytesize=8, timeout=0)

print("conn: " + ser.portstr)
# initializes the data_spg array
display_stuff.plot_init()

try:
    while(1):
        # collecting data from sensors
        cnt = ser.in_waiting
        if(cnt > 0):
            data = ser.read(cnt)
            # data is read from device, processed, and saved into umyo_get_list
            umyo_parser.umyo_parse_preprocessor(data)
            # .plot_prepare saves FTT processed emg data into 4 frequency-domain bins in plot_spg[][]
            display_stuff.plot_prepare(umyo_parser.umyo_get_list())
            first_data_stream = []
            # there is some delay with the sensor so,
            # an if statement to check if it doesn't contain 800
            # buffer zeros
            if len(display_stuff.plot_spg[0]) < 5:
                # for-loop to iterate over the individual bin data values
                for index, bin_value in enumerate(display_stuff.plot_spg[0]):
                    # print(f"Bin {index} is {bin_value}")
                    first_data_stream.append(bin_value)
                current_time = datetime.datetime.now()
                first_data_stream.append(current_time)
                full_data_stream.append(first_data_stream)
                # check if buffer is full and write to csv if it is
                if len(full_data_stream) >= buffer_size:
                    save_data_to_csv(full_data_stream, filename)
except KeyboardInterrupt:
    # Handle graceful shutdown on user interruption (Ctrl+C)
    print("Data stream interrupted by user. Saving remaining data...")
    if full_data_stream:
        save_data_to_csv(full_data_stream, filename)

