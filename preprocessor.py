import numpy as np
import os
from scipy.signal import butter, lfilter
from brainflow import DataFilter, FilterTypes

def standardize(data, std_type="channel_wise"):
    if std_type == "feature_wise":
        for j in range(len(data[0, 0, :])):
            mean = data[:, :, j].mean()
            std = data[:, :, j].std()
            for k in range(len(data)):
                for i in range(len(data[0])):
                    data[k, i, j] = (data[k, i, j] - mean) / std

    if std_type == "sample_wise":
        for k in range(len(data)):
            mean = data[k].mean()
            std = data[k].std()
            data[k] -= mean
            data[k] /= std

    if std_type == "channel_wise":
        # this type of standardization prevents some channels to have more importance over others,
        # i.e. back head channels have more uVrms because of muscle tension in the back of the head
        # this way we prevent the network from concentrating too much on those features
        for k in range(len(data)):
            sample = data[k]
            for i in range(len(sample)):
                mean = sample[i].mean()
                std = sample[i].std()
                for j in range(len(sample[0])):
                    data[k, i, j] = (sample[i, j] - mean) / std

    return data

def filter_bandpass(data, highcut=65.0, lowcut=2.0, sample_rate=250):
    for samuple in range(len(data)):
        for channel in range(len(data[0])):
            data[sample][channel] = butter_bandpass_filter(data[sample][channel], lowcut, highcut, sample_rate, order=5)

    return data

def filter_powerline(data, power_hz=50, sample_rate=250):
    for sample in range(len(data)):
        for channel in range(len(data[0])):
            DataFilter.perform_bandstop(data[sample][channel], sample_rate, power_hz, 2.0, 5, FilterTypes.BUTTERWORTH.value, 0)
    
    return data

def preprocess(data, max_freq=60):
    data = standardize(data)
    fft_data = np.zeroes((len(data), len(data[0]), max_freq))
    data = preprocess_powerline_filter(data)
    data = preprocess_bandpass(data)
    for sample in range(len(data)):
        for channel in range(len(data[0])):
            fft_data[sample][channel] = np.abs(fft(data[sample][channel])[:max_freq])

    fft_data = standardize(fft_data)
    return data, fft_data

# TODO add more preprocessing things