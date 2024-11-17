import numpy as np
import os
import time
import pickle
import collect
from collect import COLS, board_id
from brainflow.data_filter import DataFilter, FilterTypes
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds


def predict():
    suffix = "2"
    with open("fmodel{suffix}.pkl", "rb") as f:
        clf = pickle.load(f)
    print(clf)

    board = collect.prepare_session()
    X = np.array(())
    y = np.array(())

    input("Start Stream?")
    board.start_stream()
    time.sleep(1)

#     plt.ion()
#     grapha = plt.plot((), ())[0]
#     graphb = plt.plot((), ())[0]
#     graphc = plt.plot((), ())[0]
#     graphd = plt.plot((), ())[0]

    total = 0
    steps = 600
    window = np.array(())
    for i in range(steps):
#         plt.pause(1.4)
        current_data = board.get_current_board_data(COLS)
#         print(type(current_data))
#         print(current_data.shape)
#         print(current_data)
        eeg_channels = board.get_eeg_channels(board_id)
        eeg_data = current_data[eeg_channels]
        # filter in place
        for channel in range(eeg_data.shape[0]):
            DataFilter.remove_environmental_noise(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 2)
            DataFilter.perform_bandpass(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 5.0, 20.0, 5, FilterTypes.BUTTERWORTH, 0)
            DataFilter.perform_lowpass(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 20.0, 5, FilterTypes.BUTTERWORTH, 1)
            DataFilter.perform_highpass(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 1.0, 4, FilterTypes.BUTTERWORTH, 0)
#         print(eeg_data.shape)
        os.system("clear")
        prediction = clf.predict(eeg_data.flatten().reshape(1, -1))[0]
        window = np.append(window, prediction)
        if len(window) > 100:
            window = window[-100:]
        print(int(prediction), int(np.round(window.mean())))
#         X = X.reshape((-1, width))

#         grapha.remove()
#         grapha = plt.plot(np.arange(eeg_data.shape[1]), eeg_data[3], color="yellow")[0]
#         graphb.remove()
#         graphb = plt.plot(np.arange(eeg_data.shape[1]), eeg_data[0], color="red")[0]
#         graphc.remove()
#         graphc = plt.plot(np.arange(eeg_data.shape[1]), eeg_data[1], color="green")[0]
#         graphd.remove()
#         graphd = plt.plot(np.arange(eeg_data.shape[1]), eeg_data[2], color="blue")[0]

    print("Ending stream")
    board.stop_stream()


if __name__ == "__main__":
    predict()
