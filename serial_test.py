#kinda main

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

while(1):
    cnt = ser.in_waiting
    if(cnt > 0):
        data = ser.read(cnt)
        umyo_parser.umyo_parse_preprocessor(data)
        dat_id = display_stuff.plot_prepare(umyo_parser.umyo_get_list())
        d_diff = dat_id - last_data_upd
        if(d_diff > 1):
            display_stuff.draw_cycle()
            last_data_upd = dat_id

