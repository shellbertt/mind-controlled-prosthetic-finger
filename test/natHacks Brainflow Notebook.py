#!/usr/bin/env python
# coding: utf-8

# # natHacks Brainflow Tutorial

# Written by Harrison Fah for use in the natHacks workshop on November 8th, 2024. If you run this in Google Collab instead of Jupyter Notebook it should still work for the synthetic board but you will not be able to use your EEG device.

# ## Install libraries
# 
# Running this code will automatically install the libraries needed for this notebook.

# In[ ]:


# get_ipython().system('python -m pip install brainflow')
# get_ipython().system('python -m pip install numpy')
# get_ipython().system('python -m pip install matplotlib')


# ## Import libraries

# In[ ]:


from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import numpy as np
import matplotlib.pyplot as plt
import time

breakpoint()

# ## Define your device's serial port and board ID
# 
# The serial port can be found by following the instructions given in the slides.
# 
# The board ID can be found at https://brainflow.readthedocs.io/en/stable/UserAPI.html#brainflow-board-shim

# In[ ]:


params = BrainFlowInputParams()
params.serial_port = 'COM5' #Change this depending on your device and OS
board_id = 38 #Change this depending on your device


# ## Create board object
# 
# We now create the BoardShim object that allows us to interact with our device. We first try to create the object using the above parameters. We call prepare_session using the board to verify that the device is properly connected. If there is an issue with the device then it will instead create a synthetic board object. Finally we release the session from the board so that we don't run into any issues trying to prepare a session later (you can only prepare one session at a time).

# In[ ]:


#Prepares the board for reading data
try:
    board_id = 38
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


# ## Read data from board
# 
# Here we start a stream from the board so that we can record data from it. We first prepare the board and start the stream, then we wait 5 seconds and get the board data (clearing the buffer).

# In[ ]:


print("Starting Stream")
board.prepare_session()
board.start_stream()
time.sleep(5) #wait 5 seconds
data = board.get_board_data() #gets all data from board and removes it from internal buffer
print("Ending stream")
board.stop_stream()
board.release_session()


# This shows us that the data is of type numpy array and shape (nChannels, nSamples) where each row is all the sampled for that specific channel.

# In[ ]:


print(type(data))
print(data.shape)


# We can see from the result of the above code snippet that there are 32 channels, however the OpenBCI only has 16 channels. This is because Brainflow can also record other types of biosignals (EMG, EOG, ...). We are only interested in the EEG channels currently so we isolate the channels below.

# In[ ]:


#We want to isolate just the eeg data
eeg_channels = board.get_eeg_channels(board_id)
print(eeg_channels)
eeg_data = data[eeg_channels]
print(eeg_data.shape)


# In[ ]:


print(eeg_data)


# We can also find the channels for other datatypes

# In[ ]:


#We can also find the channels for other datatypes
eog_channels = board.get_eog_channels(board_id)
print(eog_channels)


# Here we plot out the data from the first EEG channel across the 5 seconds

# In[ ]:


#Plot the first EEG channel
plt.plot(np.arange(eeg_data.shape[1]), eeg_data[0])


# ## Read data and insert markers
# 
# If you are dealing with any sort of stimulus or events in your EEG data, it is handy to know where exactly they occurred. Luckily, Brainflow has a function for this, allowing you to insert markers in the datastream right when events happen. These can then be accessed from the data afterwards in the same way as the other channels.

# In[ ]:


board.prepare_session()
print("Starting Stream")
board.start_stream()
#Insert a marker after every second
for i in range(5):
    time.sleep(1)
    board.insert_marker(i+1) #0 is reserved for no stimulus so inserting 0 as a marker will give an error
    print("Inserted marker:", i+1)
time.sleep(1)
data = board.get_board_data()
print("Ending stream")
board.stop_stream()
board.release_session()


# We can see below the channel indices for the EEG channels and the marker channel

# In[ ]:


eeg_channels = board.get_eeg_channels(board_id)
print(eeg_channels)
marker_channel = board.get_marker_channel(board_id)
print(marker_channel)


# Here we print out the markers data, for each sample there is an event value. By default if there is no event Brainflow inserts a 0 (so don't use 0 as a marker yourself). We can also see the markers that we inserted (if you look closely).

# In[ ]:


markers = data[marker_channel]
print(markers)


# Here we get the sample indices where we placed our markers. We can also get the sampling rate from the board and find out at what times they occurred.

# In[ ]:


#Find the sample indexes of markers that are nonzero
marker_indexes = np.nonzero(markers)[0]
print(marker_indexes)

#Gets the sampling rate of the board (samples/second)
sampling_rate = board.get_sampling_rate(board_id)
print(sampling_rate)

#Prints out the times when the markers occurred
print(marker_indexes/sampling_rate)


# ## Reading data live
# 
# Sometimes you might want to read the data while you are still recording it. Thankfully Brainflow lets you do this. You can use the get_current_board_data(n) function to grab the last n samples. Note that this does not remove the samples from the buffer so if you grab too many samples too fast you will have overlap between your data.

# In[ ]:


board.prepare_session()
print("Starting Stream")
board.start_stream()
for i in range(5):
    time.sleep(1)
    #Gets the last 25 samples from the board without removing them from the buffer
    current_data = board.get_current_board_data(25)
    print(current_data.shape)
time.sleep(1)
data = board.get_board_data()
print(data.shape)
print("Ending stream")
board.stop_stream()
board.release_session()


# ## Save data
# 
# It is easy to save data using Brainflow. You are able to write directly to a csv file so that you can access data later.

# In[ ]:


print(eeg_data.shape)
DataFilter.write_file(eeg_data, 'eeg_data_test.csv', 'w') #Writes into a csv file in the current directory

restored_data = DataFilter.read_file('eeg_data_test.csv') #Reads file back
print(restored_data.shape)

#This shows how much the saved data differs from the original data, they are very similar but not equal.
print(eeg_data - restored_data)


# ## Low and highpass filtering
# 
# Brainflow also has some handy preprocessing features for your data. Here we apply low and highpass filtering to each EEG channel.

# In[ ]:


#Genereate more eeg_data with markers for testing below
board.prepare_session()
print("Starting Stream")
board.start_stream()
#Insert a marker after every second
for i in range(5):
    time.sleep(1)
    board.insert_marker(i+1) #0 is reserved for no stimulus so inserting 0 as a marker will give an error
    print("Inserted marker:", i+1)
time.sleep(1)
data = board.get_board_data()
print("Ending stream")
board.stop_stream()
board.release_session()

eeg_channels = board.get_eeg_channels(board_id)
eeg_data = data[eeg_channels]
plt.plot(np.arange(eeg_data.shape[1]), eeg_data[0])


# In[ ]:


for channel in range(eeg_data.shape[0]):
    #Filters work in place
    DataFilter.perform_lowpass(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 50.0, 5,
                                       FilterTypes.BUTTERWORTH, 1)
    DataFilter.perform_highpass(eeg_data[channel], BoardShim.get_sampling_rate(board_id), 2.0, 4,
                                        FilterTypes.BUTTERWORTH, 0)
plt.plot(np.arange(eeg_data.shape[1]), eeg_data[0])


# ## Wavelet transform
# 
# Brainflow also includes the wavelet transformation. In the documentation they mention using the enum WaveletTypes as the wavelet parameter, however this does not work for some versions. Instead you may either have to enter a string (e.g. "db1") or the actual int value of the wavelet type you want that can be found here: https://brainflow.readthedocs.io/en/stable/UserAPI.html#brainflow-data-filter

# In[ ]:


for channel in range(eeg_data.shape[0]):
    #Applies a wavelet transformation to the current channel, not in place

    #If this line doesn't work for you, try the one below
    wavelet_coeffs, lengths = DataFilter.perform_wavelet_transform(eeg_data[channel], 1, 3)
    #wavelet_coeffs, lengths = DataFilter.perform_wavelet_transform(eeg_data[channel], "db1", 3)

    app_coefs = wavelet_coeffs[0: lengths[0]] #approximation coefficients
    detailed_coeffs_first_block = wavelet_coeffs[lengths[0]: lengths[1]] #detailed coefficients

    #Perform an inverse wavelet transformation to get the original data back
    restored_data = DataFilter.perform_inverse_wavelet_transform((wavelet_coeffs, lengths), eeg_data[channel].shape[0], 1, 3)
    #restored_data = DataFilter.perform_inverse_wavelet_transform((wavelet_coeffs, lengths), eeg_data[channel].shape[0], "db1", 3)

    #Print the difference between the inverse wavelet data and the original data
    print(eeg_data[channel] - restored_data)


# ## Convert to MNE format
# 
# MNE is another library that has a lot of very useful tools for EEG data (and other biosignals). But to use it we have to modify our Brainflow data so that it works with the library. The MNE documentation can be found here: https://mne.tools/stable/index.html

# In[ ]:


# get_ipython().system('python -m pip install -q mne')


# In[ ]:


import mne

#Get info from board needed for conversion
eeg_channels = board.get_eeg_channels(board_id)
sampling_rate = board.get_sampling_rate(board_id)
eeg_channel_names = board.get_eeg_names(board_id)
marker_channel = board.get_marker_channel(board_id)
eeg_channel_types = ['eeg'] * len(eeg_channels)

data[eeg_channels, :] /= 1000000 #Change from microvolts to volts
mne_data = data[eeg_channels + [marker_channel], :] #Get the EEG and marker data
info = mne.create_info(ch_names=eeg_channel_names + ['stim'], sfreq=sampling_rate, ch_types=eeg_channel_types + ['stim'])
raw = mne.io.RawArray(mne_data, info) #Create MNE object
montage = mne.channels.make_standard_montage('standard_1020') #Define montage (positions of sensors)
raw.set_montage(montage)
raw.set_eeg_reference(ref_channels='average')
mne.viz.plot_montage(montage) #Displays the montage
input()

#plot without any modifications
raw.plot_psd(average=True)
input()
