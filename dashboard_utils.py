"""Standalone helpers for the Streamlit admin dashboard."""

import socket


def mask_api_key(key):
    """Mask a long API key for display, showing only the edges."""
    if not key or len(key) <= 10:
        return "None"
    return f"{key[:6]}...{key[-4:]}"


def is_port_in_use(port, host="localhost"):
    """True when something is already accepting connections on the port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0