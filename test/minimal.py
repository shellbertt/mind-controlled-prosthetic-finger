from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import numpy as np
import matplotlib.pyplot as plt
import time
import random

params = BrainFlowInputParams()
params.serial_port = 'COM5' #Change this depending on your device and OS

try:
    board_id = BoardIds.MUSE_S_BOARD
    board = BoardShim(board_id, params)
    # board.prepare_session()
    # print("Successfully prepared physical board.")
except Exception as e:
    print(e)
    exit(0)
    # #If the device cannot be found or is being used elsewhere, creates a synthetic board instead
    # print("Device could not be found or is being used by another program, creating synthetic board.")
    # board_id = BoardIds.SYNTHETIC_BOARD
    # board = BoardShim(board_id, params)
    # board.prepare_session()
# 
# board.release_session()

# board.prepare_session()
# print("Starting Stream")
# board.start_stream()
# time.sleep(5) #wait 5 seconds
# data = board.get_board_data() #gets all data from board and removes it from internal buffer
# print("Ending stream")
# board.stop_stream()
# board.release_session()
# 
# print(type(data))
# print(data.shape)
# 
# eeg_channels = board.get_eeg_channels(board_id)
# print(eeg_channels)
# eeg_data = data[eeg_channels]
# print(eeg_data.shape)
# 
# print(eeg_data)
# 
# # eog_channels = board.get_eog_channels(board_id)
# # print(eog_channels)
# 
# plt.plot(np.arange(eeg_data.shape[1]), eeg_data[0])
# plt.show()

board.prepare_session()
print("Starting Stream")
board.start_stream()
plt.ion()
graph = plt.plot([], [])[0]
plt.pause(1)
time.sleep(1)
current_data  = board.get_board_data(10)
for i in range(100):
    time.sleep(.1)

    graph.remove()
    # Gets the last 25 samples from the board without removing them from the buffer
    current_data = np.concatenate((current_data, board.get_board_data(10)), axis=1)
    eeg_channels = board.get_eeg_channels(board_id)
    eeg_data = current_data[eeg_channels]
    graph = plt.plot(np.arange(eeg_data.shape[1]), eeg_data[0])[0]
    print(current_data.shape)

#     y = [random.randint(1,10) for i in range(20)]
#     x = [*range(1,21)]
#     graph = plt.plot(x,y)[0]
    plt.pause(0.25)

data = board.get_board_data()
print(data.shape)
print("Ending stream")
board.stop_stream()
board.release_session()
