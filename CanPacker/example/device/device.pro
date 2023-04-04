TEMPLATE = app
CONFIG += console
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += \
        CAN_DEVICE.c \
        main.c

HEADERS += \
    CAN_DEVICE.h \
    CAN_DEVICE_Glue.h
