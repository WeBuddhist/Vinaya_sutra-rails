#!/bin/sh
R="/d/Work/OpenPecha/Vinaya_sutra-rails/1-SOURCES/Text/འདུལ་བ་མདོ་རྩ་བ།.md"
for p in "$@"; do printf -- "-- %s: " "$p"; grep "$p" "$R" | grep -o '\^[0-9a-zI-]*\s*$' | tr '\n' ' '; echo; done
