#!/bin/sh
export DISPLAY=:0.0
ipaddr="http://$(hostname -I)"
chromium-browser --noerrdialogs --kiosk --incognito --disable-infobars --disable-session-crashed-bubble --disable-translate  $ipaddr
