# SPDX-License-Identifier: Apache-2.0
#
# Board configuration for the OnePlus 11 (salami). Device-specific overrides on
# top of the shared sm85xx-common board config.

-include $(COMMON_PATH)/BoardConfigCommon.mk

# Display / recovery UI
TW_FRAMERATE := 120
TW_MAX_BRIGHTNESS := 550

# Vibrator (AIDL haptics)
TW_SUPPORT_INPUT_AIDL_HAPTICS := true
TW_SUPPORT_INPUT_AIDL_HAPTICS_FIX_OFF := true

TARGET_RECOVERY_DEVICE_MODULES += \
    libexpat \
    android.hardware.vibrator-V2-ndk

RECOVERY_LIBRARY_SOURCE_FILES += \
    $(TARGET_OUT_SHARED_LIBRARIES)/libexpat.so \
    $(TARGET_OUT_SHARED_LIBRARIES)/android.hardware.vibrator-V2-ndk.so
