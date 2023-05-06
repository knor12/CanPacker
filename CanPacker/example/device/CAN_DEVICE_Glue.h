#ifndef CAN_DEVICE_GLUE_H
#define CAN_DEVICE_GLUE_H

#include "CAN_DEVICE.h"
#include <stdint.h>
#include <stdbool.h>

extern uint32_t get_voltageUpdate();
extern void set_IO_ON_OFF(ON_OFF_t );

extern void set_voltageUpdate(uint16_t v );

extern void set_resetDeviceNow(uint32_t v );


extern uint32_t CAN_DEVICE_ticksMs(void);

/*user defined function return ticks elapsed in milliseconds since stampMs*/
extern uint32_t CAN_DEVICE_ticksSince(uint32_t stampMs);

/*user defined function that sends frames over the can bus */
extern bool CAN_DEVICE_sendFrame(uint32_t id, uint8_t * pData);
extern uint32_t get_IO();
#endif // CAN_DEVICE_GLUE_H
