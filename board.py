import argparse
import time
import numpy as np
from matplotlib import pyplot as plt

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

board = None 

def connect_to_headset(serial_port):
    global board
    params = BrainFlowInputParams()
    #params.serial_port = serial_port
    #board = BoardShim(2, params) #cython board has id 0. with daisy id 2
    board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
    board.prepare_session()
    board.start_stream()
    #time.sleep(10)
    return "connected"

def close_headset():
    board.stop_stream()
    board.release_session()
    return "disconnected"

def write_to_csv():
    return

def get_data():
    data = board.get_board_data()  # get 20 latest data points dont remove them from internal buffer
    print(data.shape)
    sample = []
    eeg_channels = BoardShim.get_eeg_channels(BoardIds.SYNTHETIC_BOARD.value)
    for channel in eeg_channels:
        sample.append(data[channel])

    print(np.array(sample).shape)
    for j in range(7, 8):
        plt.plot(np.arange(len(sample[j])), sample[j])
    plt.show()

    #save_sample(np.array(sample), ACTIONS[last_act])
    return None


def main():
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(10)
    data = board.get_current_board_data() # get 20 latest data points dont remove them from internal buffer
    board.stop_stream()
    board.release_session()

    # demo how to convert it to pandas DF and plot data
    eeg_channels = BoardShim.get_eeg_channels(BoardIds.SYNTHETIC_BOARD.value)
    df = pd.DataFrame(np.transpose(data))
    print('Data From the Board')
    print(df.head(10))

    # demo for data serialization using brainflow API, we recommend to use it instead pandas.to_csv()
    DataFilter.write_file(data, 'test.csv', 'w')  # use 'a' for append mode
    restored_data = DataFilter.read_file('test.csv')
    restored_df = pd.DataFrame(np.transpose(restored_data))
    print('Data From the File')
    print(restored_df.head(10))


if __name__ == "__main__":
    main()