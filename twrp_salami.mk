# SPDX-License-Identifier: Apache-2.0
#
# Product configuration for PitchBlack Recovery on the OnePlus 11 (salami).

# Common folder identifier and hardware platform
COMMON_SOC := sm85xx
PRODUCT_PLATFORM := kalama

# Paths
COMMON_PATH := device/oneplus/sm85xx-common
DEVICE_PATH := device/oneplus/salami

# Inherit from the recovery product configuration
$(call inherit-product, vendor/twrp/config/common.mk)

# Device identifiers
PRODUCT_DEVICE := salami
PRODUCT_NAME := twrp_salami
PRODUCT_BRAND := OnePlus
PRODUCT_MODEL := CPH2449
PRODUCT_MANUFACTURER := OnePlus
PRODUCT_SYSTEM_NAME := CPH2449
PRODUCT_SYSTEM_DEVICE := OP594DL1

PRODUCT_BUILD_PROP_OVERRIDES += \
    TARGET_DEVICE=OP594DL1 \
    TARGET_PRODUCT=CPH2449

# Inherit the hardware-specific configuration
$(call inherit-product, $(DEVICE_PATH)/device-salami.mk)
