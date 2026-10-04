#!/bin/bash

# ==============================================================================
# RPLIDAR ROS2 DRIVER
#
# udev Rules Setup Script
#
# This script creates a persistent symbolic device link `/dev/rplidar`
# for Slamtec RPLIDAR devices using the Silicon Labs CP210x USB-UART chipset.
#
# The rule matches the device by Vendor ID and Product ID and assigns:
#   - MODE  = 0666           (world-readable/writable)
#   - GROUP = dialout        (typical serial-device group on Ubuntu)
#   - SYMLINK = rplidar      (/dev/rplidar)
#
# NOTE:
#   If other devices on your system share the same chipset
#   (e.g., ESP32 boards using CP210x), you may need to refine the rule
#   further by matching the device serial number.
#
# Author: frozenreboot
# ==============================================================================

echo "================================================================="
echo "RPLIDAR udev rules setup"
echo "================================================================="
echo "This script will configure a persistent device alias:"
echo "    /dev/rplidar"
echo ""
echo "Default chipset assumed: Silicon Labs CP210x"
echo "================================================================="

# Default USB Vendor/Product IDs for Silicon Labs CP210x
ID_VENDOR="10c4"
ID_PRODUCT="ea60"
SYMLINK_NAME="rplidar"
RULES_FILE="/etc/udev/rules.d/99-rplidar.rules"

echo ""
echo "Creating udev rule for device ID ${ID_VENDOR}:${ID_PRODUCT}"
echo " -> /dev/${SYMLINK_NAME}"
echo ""

# Write udev rule
# MODE=0666 allows non-root access
echo "KERNEL==\"ttyUSB*\", ATTRS{idVendor}==\"${ID_VENDOR}\", ATTRS{idProduct}==\"${ID_PRODUCT}\", MODE:=\"0666\", GROUP:=\"dialout\", SYMLINK+=\"${SYMLINK_NAME}\"" \
| sudo tee "${RULES_FILE}"

echo ""
echo "-----------------------------------------------------------------"
echo "Reloading udev rules..."
echo "-----------------------------------------------------------------"
sudo udevadm control --reload-rules
sudo udevadm trigger

echo ""
echo "Done!"
echo ""
echo "Verify using:"
echo "  ls -l /dev/${SYMLINK_NAME}"
echo ""
echo "If the link does not appear, unplug and reconnect the RPLIDAR."
echo "-----------------------------------------------------------------"
