#include <stdio.h>
#include "CAN_DEVICE.h"

uint32_t  get_voltageUpdate(){return 10; }

void set_IO_ON_OFF(ON_OFF_t IO_){ printf("io set to %d\n", IO_); }
void set_voltageUpdate(uint16_t v ){printf("voltage update %d\n", v); }
void set_resetDeviceNow(uint32_t v ){ printf("reset 0x%x\n", v);  }


int main()
{
    uint64_t data = 0;
    uint16_t current;

    bool ret = HEALTH_pack(    10/*const uint32_t ID*/,
                    (uint8_t*)&data/*uint8_t * pU8Data*/
                    /*uint32_t HEALTH_MULTIPLEXOR */ /*key */ /*is a constant no argument is used*/
                    /*uint16_t  VOLTAGe_HEALTH */  /*value gotton from get_voltageUpdate()*/ ,
                    22/*const uint16_t  CURRENTHEALTH*/ ,
                    OFF/*const ON_OFF_t  IO*/);

    printf("ret = %d\n", ret);

    HEALTH_unpack(    10 /*const uint32_t ID*/,
                      (uint8_t*)&data/*uint8_t * pU8Data*/
                      /*uint32_t HEALTH_MULTIPLEXOR*/ /*key */ /*is a constant no argument is used*/
                      /*uint16_t * VOLTAGe_HEALTH*/  /*value set to set_voltageUpdate()*/ ,
                      &current/*uint16_t * CURRENTHEALTH*/
                      /*ON_OFF_t * IO*/  /*value set to set_IO_ON_OFF()*/ );
    return 0;
}
