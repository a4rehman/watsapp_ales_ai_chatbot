"""Tests for dashboard helpers (no Streamlit/Node dependencies)."""

import os
import socket
import sys
import threading

sys.path.insert(0, os.path.dirname(__file__))

from dashboard_utils import mask_api_key, is_port_in_use


def test_mask_api_key_long():
    assert mask_api_key("1234567890abcdefghijklmnop") == "123456...mnop"


def test_mask_api_key_short_returns_none():
    assert mask_api_key("shortkey") == "None"


def test_mask_api_key_empty():
    assert mask_api_key("") == "None"
    assert mask_api_key(None) == "None"


def test_mask_api_key_keeps_mid_hidden():
    key = "A" * 50
    masked = mask_api_key(key)
    assert masked.startswith("AAAAAA...")
    assert masked.endswith("AAAA")
    assert len(masked) < len(key)


def test_is_port_in_use_detects_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.bind(("localhost", 0))
        srv.listen(1)
        port = srv.getsockname()[1]
        assert is_port_in_use(port)


def test_is_port_in_use_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 0))
        port = s.getsockname()[1]
    assert not is_port_in_use(port)


if __name__ == "__main__":
    for name, fn in sorted(list(globals().items())):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("ALL DASHBOARD UTIL TESTS PASSED")