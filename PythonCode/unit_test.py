import pytest
from hub_data_rx import packet_decode
from node_data_tx import packet_encode
import time


def test_encode():
    test_pack = packet_encode(12.34567, 12.34567, 1)
