import os
import re
import numpy as np

def load_data_from_log_files(data_dir):
    payloads = list()
    for file in os.listdir(data_dir):
        with(open(data_dir + file)) as f:
            lines = f.readlines()
            for i in range(lines.__len__()):
                split = re.split("(GET|HEAD|POST|DELETE|OPTIONS|PUT|TRACE|CONNECT|PROPFIND)", lines[i])
                lines[i] = re.split("(HTTP/1.1|HTTP/1.0)", (split[1] + split[2]))[0]
            payloads.extend(lines)
    return payloads


def load_preprocessed_payloads_from_file(filename, data_dir=''):
    with(open(filename, 'r')) as file:
        lines = file.readlines()
    return lines


def save_to_file(filename, data_dir):
    with(open(filename, 'w+')) as out:
        for p in load_data_from_log_files(data_dir):
            out.write(p + "\n")


def count_freqs(payloads):
    occurences = np.zeros(256, dtype=np.uint64)
    freqs = np.zeros(256, dtype=np.double)
    payloads_len = 0
    for idx, payload in enumerate(payloads):
        payloads_len += len(payload)
        for char in payload:
            occurences[ord(char)] += 1
    if payloads_len != 0:
        for i in range(256):
            freqs[i] = occurences[i] / payloads_len
    mean = freqs.mean()
    devs = freqs - mean
    return freqs, occurences, devs


def count_std_dev(freqs):
    return freqs.std()


if __name__ == "__main__":
    a = load_preprocessed_payloads_from_file('output.csv')

    freqs = count_freqs(a)[0]
    for idx, mean in enumerate(freqs):
        print(chr(idx) + " : " + str(mean))
    print(freqs.sum())
    print()
