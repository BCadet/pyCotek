
import logging
from pyftdi.i2c import I2cController

class UMFT200XDI2CBUS:
    """Custom I2C Class"""

    # pylint: disable=unused-argument
    def __init__(self, url='ftdi:///1', slave=0x01):
        self.ftdi = I2cController()
        self.ftdi.configure(url)
        self.slave = slave
        self.log = logging.getLogger('UMFT200XDI2CBUS')
        # self.log.setLevel(logging.DEBUG)
        self.log.debug('init')
        
    def try_lock(self):
        return True
    
    def unlock(self):
        return True
        
    def scan(self):
        self.log.debug('scan')
        """Perform an I2C Device Scan"""
        return [addr for addr in range(0x79)] # HACK: all addresses are valid (la flem !)

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        """Write data from the buffer to an address"""
        self.log.debug(f'writeto {address=} {buffer=} {start=} {end=}')
        port = self.ftdi.get_port(self.slave)
        port.write_to(address, buffer)
        

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
        """Read data from an address and into the buffer"""
        self.log.debug(f'readfrom_into  {address=} {buffer=} {start=} {end=}')
        self.log.debug(f'{len(buffer)=}')
        


    # pylint: disable=unused-argument
    def writeto_then_readfrom(
        self,
        address,
        buffer_out,
        buffer_in,
        *,
        out_start=0,
        out_end=None,
        in_start=0,
        in_end=None,
        stop=False,
    ):
        """Write data from buffer_out to an address and then
        read data from an address and into buffer_in
        """
        self.log.debug('writeto_then_readfrom')
        out_end = out_end if out_end else len(buffer_out)
        in_end = in_end if in_end else len(buffer_in)
        self.writeto(address, buffer_out, start=out_start, end=out_end)
        self.readfrom_into(address, buffer_in, start=in_start, end=in_end)
