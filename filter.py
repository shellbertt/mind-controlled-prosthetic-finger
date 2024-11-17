from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import numpy as np
import matplotlib.pyplot as plt
from collect import COLS, board_id
from concatenate import info


suffix = "78"
X = np.load(f"backup/X{suffix}.npy")
y = np.load(f"backup/y{suffix}.npy")

info(X, y)

plt1 = plt.subplot2grid((1, 2), (0, 0))
for i in [5]:
    plt1.plot(np.arange(X[i].shape[1]), X[i][0], color="red")[0]
    plt1.plot(np.arange(X[i].shape[1]), X[i][1], color="green")[0]
    plt1.plot(np.arange(X[i].shape[1]), X[i][2], color="blue")[0]
    plt1.plot(np.arange(X[i].shape[1]), X[i][3], color="yellow")[0]

# filter in place
for i in range(len(X)):
    for channel in range(X[i].shape[0]):
        continue
        DataFilter.perform_bandpass(X[i][channel], BoardShim.get_sampling_rate(board_id), 5.0, 20.0, 1, FilterTypes.BUTTERWORTH, 0)
#         DataFilter.remove_environmental_noise(X[i][channel], BoardShim.get_sampling_rate(board_id), 2)
#         DataFilter.perform_lowpass(X[i][channel], BoardShim.get_sampling_rate(board_id), 20.0, 5, FilterTypes.BUTTERWORTH, 1)
#         DataFilter.perform_highpass(X[i][channel], BoardShim.get_sampling_rate(board_id), 1.0, 4, FilterTypes.BUTTERWORTH, 0)

plt2 = plt.subplot2grid((1, 2), (0, 1))
for i in [5]:
    plt2.plot(np.arange(X[i].shape[1]), X[i][0], color="red")[0]
    plt2.plot(np.arange(X[i].shape[1]), X[i][1], color="green")[0]
    plt2.plot(np.arange(X[i].shape[1]), X[i][2], color="blue")[0]
    plt2.plot(np.arange(X[i].shape[1]), X[i][3], color="yellow")[0]

plt.show()

Xnew = np.array(())
ynew = np.array(())
width = 100
step = width
for i in range(len(X)):
    print(i, X[i].shape[1])
    for j in range(width, X[i].shape[1]+1, step):
        # print(f"add {j-COLS=} {j=} {pred=}")
        app = X[i][:,j-width:j].flatten()
        if len(Xnew) == 0:
            Xnew = app
        else:
            Xnew = np.vstack((Xnew, app))
        ynew = np.append(ynew, y[i])

X = Xnew
y = ynew

print("new")
info(Xnew, ynew)

np.save(f"backup/X{suffix}Filtered.npy", X)
np.save(f"backup/y{suffix}Filtered.npy", y)


