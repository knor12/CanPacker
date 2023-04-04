#ifndef CAN_DEVICE_GLUE_H
#define CAN_DEVICE_GLUE_H

#include "CAN_DEVICE.h"
#include <stdint.h>

extern uint32_t get_voltageUpdate();
extern void set_IO_ON_OFF(ON_OFF_t );

extern void set_voltageUpdate(uint16_t v );

extern void set_resetDeviceNow(uint32_t v );

#endif // CAN_DEVICE_GLUE_H
