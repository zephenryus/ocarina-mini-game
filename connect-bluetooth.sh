#!/bin/bash
# Replace <MAC_ADDRESS> with your Bluetooth device's MAC address
BLUETOOTH_DEVICE="10:28:74:F4:4B:EC"

# Attempt to connect to the Bluetooth device
bluetoothctl << EOF
power on
connect $BLUETOOTH_DEVICE
EOF
