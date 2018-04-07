#!/bin/bash
set -eufo pipefail

apt-get install \
    python3-gi \
    libwebkitgtk-3.0-0 \
    libwebkitgtk-3.0-dev
