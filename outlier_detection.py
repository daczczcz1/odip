import numpy as np
import os
from config import DATA_DIR
from process_data import load_preprocessed_payloads_from_file, count_std_dev, count_freqs


class Model:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.freqs = np.zeros(256, dtype=np.double)
        self.variance = np.zeros(256, dtype=np.double)
        self.dev = np.zeros(256, dtype=np.double)

    def train(self, input_file):
        data = load_preprocessed_payloads_from_file(input_file)
        stats = count_freqs(data)
        self.freqs = stats[0]
        self.dev = stats[2]

    def save_to_file(self, filename, dir=''):
        with(open(dir + '/' + filename, 'w')) as f:
            f.write(np.array2string(self.freqs, max_line_width=5120).replace("[", "").replace("]", "") + "\n")
            f.write(np.array2string(self.dev, max_line_width=5120).replace("[", "").replace("]", ""))

    def load_from_file(self, filename, dir=''):
        with(open(dir + '/' + filename, 'r')) as f:
            self.freqs = np.fromstring(f.readline(), dtype=np.double, count=256, sep=' ')
            self.dev = np.fromstring(f.readline(), dtype=np.double, count=256, sep=' ')

    def evaluate(self, payload):
        payload_freq = count_freqs(payload)


    def update(self, payloads):
        pass


def simplified_mahalanobis(x, y):
    if x.shape != y.shape:
        raise ValueError("The vectors passed should be of same shape (x.shape = " + x.shape + ", y.shape = " + y.shape)



if __name__ == '__main__':
    # test
    a = Model(DATA_DIR)
    a.train('output_small.csv')
    print("CALCULATED")
    print(a.freqs)

    print(a.dev)
    a.save_to_file('calculated.csv', dir=os.getcwd())
    print("+++++++++++++++++++++++++++")
    a.load_from_file('calculated.csv', dir=os.getcwd())
    print("LOADED")

    print(a.freqs)
    print(a.dev)
