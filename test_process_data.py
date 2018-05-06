import process_data
import numpy as np


def test_count_freqs_basic():
    allchars = [chr(i) for i in range(256)]
    payloads = ""
    payloads = payloads.join(allchars)
    expected = np.zeros(256, dtype=np.double)
    expected += 1 / 256
    assert expected.all() == process_data.count_freqs(payloads)[0].all()


def test_count_freqs_empty():
    payloads = ["", ]
    expected = np.zeros(256, dtype=np.double)
    assert expected.all() == process_data.count_freqs(payloads)[0].all()

