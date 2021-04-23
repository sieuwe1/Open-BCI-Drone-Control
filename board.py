import argparse
import time
import numpy as np
from matplotlib import pyplot as plt
import os

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

board = None 
data_dir = None

def connect_to_headset(serial_port):
    global board
    params = BrainFlowInputParams()
    params.serial_port = serial_port
    board = BoardShim(BoardIds.CYTON_DAISY_BOARD, params) #cython board has id 0. with daisy id 2
    #board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params) fake board
    board.prepare_session()
    return "connected"

def close_headset():
    board.stop_stream()
    board.release_session()
    return "disconnected"

def write_to_csv():
    return

def start_data_stream():
    board.start_stream()

def stop_data_stream():
    data = board.get_current_board_data(250)
    board.stop_stream()

    sample = []
    eeg_channels = BoardShim.get_eeg_channels(BoardIds.CYTON_DAISY_BOARD.value)
    #print("channels = " + str(eeg_channels))
    for channel in eeg_channels:
        sample.append(data[channel])
    return sample

def create_directory(directoy_name):
    global data_dir
    if not os.path.exists(directoy_name):
        os.mkdir(directoy_name)
    data_dir = directoy_name

def save_sample(sample, action):
    actiondir = f"{data_dir}/{action}"
    if not os.path.exists(actiondir):
        os.mkdir(actiondir)

    print(f"saving {action} personal_dataset...")
    np.save(os.path.join(actiondir, f"{int(time.time())}.npy"), np.array(sample))