from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import numpy as np
import matplotlib.pyplot as plt
import time


board_id = BoardIds.SYNTHETIC_BOARD
board_id = BoardIds.GANGLION_BOARD
COLS = 200


def prepare_session():
    params = BrainFlowInputParams()
    params.serial_port = "/dev/ttyACM0"
    board = BoardShim(board_id, params)
    board.prepare_session()
    return board


def collect(board):
    X = np.array(())
    y = np.array(())

    input("Start Stream?")
    board.start_stream()

    plt.ion()
    grapha = plt.plot((), ())[0]
    graphb = plt.plot((), ())[0]
    graphc = plt.plot((), ())[0]
    graphd = plt.plot((), ())[0]

    current_data = board.get_board_data()
    total = 0
    steps = 8
    for i in range(steps):
        pred = i % 2 == 0
        print("SQUEEZE" if pred else "RELAX")
        plt.pause(14)
        current_data = board.get_board_data(COLS * 12)
        print(type(current_data))
        print(current_data.shape)
        print(current_data)
        eeg_channels = board.get_eeg_channels(board_id)
        eeg_data = current_data[eeg_channels]
        print(eeg_data.shape)
        if i >= 2:
            total += len(eeg_data.flatten())
            if len(X) == 0:
                X = np.array([eeg_data])
            else:
                X = np.vstack((X, np.array([eeg_data])))
            y = np.append(y, pred)

        grapha.remove()
        grapha = plt.plot(np.arange(eeg_data.shape[1]), eeg_data[3], color="yellow")[0]
        graphb.remove()
        graphb = plt.plot(np.arange(eeg_data.shape[1]), eeg_data[0], color="red")[0]
        graphc.remove()
        graphc = plt.plot(np.arange(eeg_data.shape[1]), eeg_data[1], color="green")[0]
        graphd.remove()
        graphd = plt.plot(np.arange(eeg_data.shape[1]), eeg_data[2], color="blue")[0]

    print("Ending stream")
    board.stop_stream()

    width = COLS * len(eeg_channels)
    print(X.shape, y.shape, width, total)
#     X = X.reshape((-1, width))
    return (X, y)


if __name__ == "__main__":
    board = prepare_session()
    X, y = collect(board)
    print("X")
    print(X)
    print(X.shape)
    print("y")
    print(y)
    print(y.shape)
    np.save("X", X)
    np.save("y", y)
    board.release_session()


