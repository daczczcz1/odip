import numpy as np
import os
from config import DATA_DIR, ALPHA
from process_data import load_preprocessed_payloads_from_file, count_mean_freqs, count_std_devs


class Model:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.freqs = np.zeros(256, dtype=np.double)
        self.variance = np.zeros(256, dtype=np.double)
        self.dev = np.zeros(256, dtype=np.double)

    def train(self, input_file):
        data = load_preprocessed_payloads_from_file(input_file)
        freqs = count_mean_freqs(data)
        devs = count_std_devs(data)
        self.freqs = freqs
        self.dev = devs

    def save_to_file(self, filename, dir=''):
        with(open(dir + '/' + filename, 'w')) as f:
            f.write(np.array2string(self.freqs, max_line_width=5120).replace("[", "").replace("]", "") + "\n")
            f.write(np.array2string(self.dev, max_line_width=5120).replace("[", "").replace("]", ""))

    def load_from_file(self, filename, dir=''):
        with(open(dir + '/' + filename, 'r')) as f:
            self.freqs = np.fromstring(f.readline(), dtype=np.double, count=256, sep=' ')
            self.dev = np.fromstring(f.readline(), dtype=np.double, count=256, sep=' ')

    def evaluate(self, payload):
        payload_freqs = count_mean_freqs(payload)
        print(payload_freqs)
        print(simplified_mahalanobis(self.freqs, payload_freqs, self.dev))
        #     Todo

    def update(self, payloads):
        pass
#     Todo


def simplified_mahalanobis(x_freqs, y_freqs, devs):
    if x_freqs.shape != y_freqs.shape or y_freqs.shape != devs.shape or x_freqs.shape != (256, ):
        raise ValueError("The vectors passed should be of same shape (x.shape = " + x_freqs.shape + ", y.shape = " + y_freqs.shape + ", devs.shape = " + devs.shape)
    return np.absolute((x_freqs - y_freqs)/(devs + ALPHA)).sum()


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
    print("PAYLOAD:")
    a.evaluate("index.html")
