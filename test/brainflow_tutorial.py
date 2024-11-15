from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import numpy as np
import matplotlib.pyplot as plt
import time

params = BrainFlowInputParams()
params.serial_port = 'COM5' #Change this depending on your device and OS
board_id = -1 #Change this depending on your device

#Prepares the board for reading data
try:
    board = BoardShim(board_id, params)
    board.prepare_session()
    print("Successfully prepared physical board.")
except Exception as e:
    print(e)
    #If the device cannot be found or is being used elsewhere, creates a synthetic board instead
    print("Device could not be found or is being used by another program, creating synthetic board.")
    board_id = BoardIds.SYNTHETIC_BOARD
    board = BoardShim(board_id, params)
    board.prepare_session()
#Releases the board session
board.release_session()

print("Starting Stream")
board.prepare_session()
board.start_stream()
time.sleep(5) #wait 5 seconds
data = board.get_board_data() #gets all data from board and removes it from internal buffer
print("Ending stream")
board.stop_stream()
board.release_session()

print(type(data))
print(data.shape)

#We want to isolate just the eeg data
eeg_channels = board.get_eeg_channels(board_id)
print(eeg_channels)
eeg_data = data[eeg_channels]
print(eeg_data.shape)

print(eeg_data)
