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


def count_mean_freqs(payloads):
    probababilities_sums = np.zeros(256, dtype=np.double)
    result = np.zeros(256, dtype=np.double)
    counter = 0
    for payload in payloads:
        occurrences_in_payload = np.zeros(256, dtype=np.uint64)
        if len(payload) > 0:
            for char in payload:
                occurrences_in_payload[ord(char)] += 1
            probababilities_sums += occurrences_in_payload / len(payload)
        counter += 1
    if counter > 0:
        result = probababilities_sums / counter
    return result


def count_std_devs(payloads):
    mean_freqs = count_mean_freqs(payloads)
    devs_sums = np.zeros(256, dtype=np.double)
    result = np.zeros(256, dtype=np.double)
    counter = 0
    for payload in payloads:
        occurrences_in_payload = np.zeros(256, dtype=np.uint64)
        if len(payload) > 0:
            for char in payload:
                occurrences_in_payload[ord(char)] += 1
            devs_sums += occurrences_in_payload / len(payload) - mean_freqs
        counter += 1
    if counter > 0:
        result = devs_sums / counter
    return result


if __name__ == "__main__":
    a = ["aa", "ab", "bb"]

    freqs = count_mean_freqs(a)
    for idx, mean in enumerate(freqs):
        print(chr(idx) + " : " + str(mean))
    print(freqs.sum())
    print('_____________-----------------')
    devs = count_std_devs(a)
    for idx, mean in enumerate(devs):
        print(chr(idx) + " : " + str(mean))
    print(devs.sum())
