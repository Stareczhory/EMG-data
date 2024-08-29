import umyo_parser
import display_stuff

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
last_data_upd = 0
display_stuff.plot_init()
while(1):
    cnt = ser.in_waiting
    if(cnt > 0):
        data = ser.read(cnt)
        # data is read from device, processed, and saved into umyo_get_list
        umyo_parser.umyo_parse_preprocessor(data)
        # .plot_prepare saves FTT processed emg data into 4 frequency-domain bins in plot_spg[][]
        display_stuff.plot_prepare(umyo_parser.umyo_get_list())
        # for-loop to iterate over the bin data
        for index, bin_values in enumerate(display_stuff.plot_spg[0]):
            print(f"Bin {index+1} is {bin_values}")
