data_spg = []
max_devices = 64
active_devices = 0
last_data_id = [0]*max_devices
not_updated_cnt = [10000]*max_devices

def plot_init():
    global plot_emg, max_devices
    for i in range(max_devices):
        data_spg.append([0]*800)
def prepare_data(devices):
    global data_spg, max_devices, active_devices, last_data_id
    for i in range(max_devices): not_updated_cnt[i] += 1
    cnt = len(devices)
    if(cnt < 1): return
    for d in range(cnt):
        if(devices[d].data_id != last_data_id[d]):
            not_updated_cnt[d] = 0
            for n in range(4):
                data_spg[d].append(devices[d].device_spectr[n])
        last_data_id[d] = devices[d].data_id
