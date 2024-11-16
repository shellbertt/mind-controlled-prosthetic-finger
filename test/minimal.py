from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import numpy as np
import matplotlib.pyplot as plt
import time
import random

params = BrainFlowInputParams()
params.serial_port = '/dev/ttyACM0' #Change this depending on your device and OS

board_id = BoardIds.SYNTHETIC_BOARD
board_id = BoardIds.MUSE_S_BOARD
board_id = BoardIds.GANGLION_BOARD
board = BoardShim(board_id, params)

board.prepare_session()
print("Starting Stream")
board.start_stream()
plt.ion()
graph = plt.plot([], [])[0]
current_data  = board.get_board_data()
for i in range(2000):
    current_data = np.concatenate((current_data, board.get_board_data()), axis=1)[:, -200:]
#     print(type(current_data))
#     print(current_data.shape)
#     print(current_data)
    eeg_channels = board.get_eeg_channels(board_id)
    eeg_data = current_data[eeg_channels]
    for channel in range(eeg_data.shape[0]):
        DataFilter.perform_lowpass(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 50.0, 5, FilterTypes.BUTTERWORTH, 1)
        DataFilter.perform_highpass(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 2.0, 4, FilterTypes.BUTTERWORTH, 0)

    graph.remove()
    graph = plt.plot(np.arange(eeg_data.shape[1]), eeg_data[0], color="red")[0]
    plt.pause(.0001)

print("Ending stream")
board.stop_stream()
board.release_session()
