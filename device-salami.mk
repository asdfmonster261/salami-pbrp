# SPDX-License-Identifier: Apache-2.0
#
# Hardware-specific product configuration for the OnePlus 11 (salami).

# Inherit from the shared sm85xx-common configuration
$(call inherit-product, $(COMMON_PATH)/device-common.mk)

# Recovery ramdisk overlay (device vibrator/haptics HAL, variant script)
TARGET_RECOVERY_DEVICE_DIRS += $(DEVICE_PATH)/twrp
