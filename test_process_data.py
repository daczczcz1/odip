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
