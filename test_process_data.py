import process_data
import numpy as np


def test_count_freqs_basic():
    allchars = [chr(i) for i in range(256)]
    payloads = ""
    payloads = payloads.join(allchars)
    expected = np.zeros(256, dtype=np.double)
    expected += 1 / 256
    assert (expected == process_data.count_mean_freqs(payloads)).all()


def test_count_freqs_empty():
    payloads = ["", ]
    expected = np.zeros(256, dtype=np.double)
    assert (expected == process_data.count_mean_freqs(payloads)).all()


def test_count_freqs_distinct_payloads():
    payloads = ["a", "b", "c"]
    expected = np.zeros(256, dtype=np.double)
    expected[97] = 1 / 3
    expected[98] = 1 / 3
    expected[99] = 1 / 3
    assert (expected == process_data.count_mean_freqs(payloads)).all()


def test_count_freqs_distinct_payloads_of_variable_length():
    payloads = ["a", "ab", "aaac", "x", "za", "    a"]
    expected = np.zeros(256, dtype=np.double)
    expected[97] = (1 + 1 / 2 + 3 / 4 + 1 / 2 + 1 / 5) / 6
    expected[98] = (1 / 2) / 6
    expected[99] = (1 / 4) / 6
    expected[120] = 1 / 6
    expected[122] = (1 / 2) / 6
    expected[32] = (4 / 5) / 6
    assert (expected == process_data.count_mean_freqs(payloads)).all()


def test_count_devs_basic():
    allchars = [chr(i) for i in range(256)]
    payloads = ""
    payloads = payloads.join(allchars)
    expected = np.zeros(256, dtype=np.double)
    actual = process_data.count_std_devs(payloads)
    assert (expected == actual).all()


def test_count_devs_empty():
    payloads = ["", ]
    expected = np.zeros(256, dtype=np.double)
    assert (expected == process_data.count_mean_freqs(payloads)).all()


def test_count_devs_distinct_payloads():
    payloads = ["a", "b", "c"]
    expected = np.zeros(256, dtype=np.double)
    expected[97] = ((1 - 1 / 3) + (0 - 1 / 3) + (0 - 1 / 3)) / 3
    expected[98] = ((1 - 1 / 3) + (0 - 1 / 3) + (0 - 1 / 3)) / 3
    expected[99] = ((1 - 1 / 3) + (0 - 1 / 3) + (0 - 1 / 3)) / 3
    assert (expected == process_data.count_std_devs(payloads)).all()


def test_count_devs_distinct_payloads_of_variable_length():
    payloads = ["a", "ab", "aaaca", "bba"]
    expected = np.zeros(256, dtype=np.double)
    mean_a = (1 + 1 / 2 + 4 / 5 + 1 / 3) / 4
    mean_b = (1 / 2 + 2 / 3) / 4
    mean_c = (1 / 5) / 4
    expected[97] = ((1 - mean_a) + (1 / 2 - mean_a) + (4 / 5 - mean_a) + (1 / 3 - mean_a)) / 4
    expected[98] = ((0 - mean_b) + (1 / 2 - mean_b) + (0 - mean_b) + (2 / 3 - mean_b)) / 4
    expected[99] = ((0 - mean_c) + (0 - mean_c) + (1 / 5 - mean_c) + (0 - mean_c)) / 4
    actual = process_data.count_std_devs(payloads)
    assert (expected == actual).all()
