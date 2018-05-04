#!/usr/bin/env bash

$(sudo rm /usr/bin/deet*)

$(sudo rm /usr/lib/systemd/system/deet*)
$(sudo systemctl disable deet.timer)
$(sudo systemctl daemon-reload)

$(sudo rm -r /var/lib/DEET)
