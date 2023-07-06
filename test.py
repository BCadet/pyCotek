import os
os.environ["BLINKA_FT232H"] = 'ftdi://ftdi:ft-x:FTVWFBBC/1'
import logging
logging.basicConfig(format="[%(asctime)s] %(name)16s [%(levelname)8s] --- %(message)s",level=logging.DEBUG)
from cotek import Cotek
import board
import busio
import time

log = logging.getLogger('main')
i2c = busio.I2C(board.SCL, board.SDA, 50000)
# i2c.writeto(0x10, [i for i in range(50)])
# result = i2c.scan()
# print(result)
cotek = Cotek(i2c, 0)
cotek.log_infos()
cotek.log_command_state()
cotek.log_status()
cotek.voltage = 24.20
cotek.current = 1
print('enable output')
log.info(f'{cotek.internal_temp=}')
log.info(f'{cotek._output_voltage_reg/100=}')
cotek.Remote_Control = True
cotek.Power_Control = True
cotek.Command_Update = True

try:
    while(True):
        log.info(f'{cotek.voltage=}')
        log.info(f'{cotek.current=}')
        time.sleep(1)
except(KeyboardInterrupt):
    cotek.Power_Control = False
    cotek.Remote_Control = False
    exit()