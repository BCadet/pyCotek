from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bit import ROBit, RWBit
from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
import time
import datetime
import logging

'''
Cotek alimentation communication class
'''
class Cotek:
    
    '''
    Registers definition
    '''
    _MANUFACTURER = 0x00
    _MODEL = 0x10
    _OUTPUT_VOLTAGE_1 = 0x20
    _REVISION = 0x24
    _DATE_OF_MANUFACTURE = 0x28
    _SERIAL_NUMBER = 0x30
    _COUNTRY_OF_MANUFACTURE = 0x40
    _RATE_OUTPUT_VOLTAGE = 0x50
    _RATE_OUTPUT_CURRENT = 0x52
    _MAX_OUTPUT_VOLTAGE = 0x54
    _MAX_OUTPUT_CURRENT = 0x56
    _OUTPUT_VOLTAGE_2 = 0x60
    _OUTPUT_CURRENT = 0x62
    _INTERNAL_TEMPERATURE = 0x68
    _STATUS_0 = 0x6C
    _STATUS_1 = 0x6F
    _OP_VOLTAGE = 0x70
    _OP_CURRENT = 0x72
    _CONTROL = 0x7C
        
    '''
    Status bits
    '''
    _OVP_Shutdown_bit = ROBit(_STATUS_0, 0)
    _OLP_Shutdown_bit = ROBit(_STATUS_0, 1)
    _OTP_Shutdown_bit = ROBit(_STATUS_0, 2)
    _FAN_failure_bit = ROBit(_STATUS_0, 3)
    _AUX_SMPS_Failure_bit = ROBit(_STATUS_0, 4)
    _HI_TEMP_Alarm_bit = ROBit(_STATUS_0, 5)
    _AC_Input_Power_Down_bit = ROBit(_STATUS_0, 6)
    _AC_Input_Failure_bit = ROBit(_STATUS_0, 7)
    _Inhibit_VCI_ACI_INHI_bit = ROBit(_STATUS_1, 0)
    _Inhibit_Control_Register_bit = ROBit(_STATUS_1, 1)
    
    '''
    Control bits
    '''
    _Power_Control_bit = RWBit(_CONTROL, 0)
    _Command_Update_bit = RWBit(_CONTROL, 2)
    _Command_Error_bit = ROBit(_CONTROL, 3)
    _Remote_Control_bit = RWBit(_CONTROL, 7)
    
    '''
    Data Registers
    '''
    _manufacturer_reg = ROUnaryStruct(_MANUFACTURER, '<16s')
    _model_reg = ROUnaryStruct(_MODEL, '<16s')
    _revision_reg = ROUnaryStruct(_REVISION, '<4s')
    _date_of_manufacture_reg = ROUnaryStruct(_DATE_OF_MANUFACTURE, '<8s')
    _serial_reg = ROUnaryStruct(_SERIAL_NUMBER, '<16s')
    _country_reg = ROUnaryStruct(_COUNTRY_OF_MANUFACTURE, '<16s')
    _rate_output_voltage_reg = ROUnaryStruct(_RATE_OUTPUT_VOLTAGE, '<H')
    _rate_output_current_reg = ROUnaryStruct(_RATE_OUTPUT_CURRENT, '<H')
    _max_output_voltage_reg = ROUnaryStruct(_MAX_OUTPUT_VOLTAGE, '<H')
    _max_output_current_reg = ROUnaryStruct(_MAX_OUTPUT_CURRENT, '<H')
    _internal_temp_reg = ROUnaryStruct(_INTERNAL_TEMPERATURE, '<B')
    _voltmeter_reg = ROUnaryStruct(_OUTPUT_VOLTAGE_2, '<H')
    _ammeter_reg = ROUnaryStruct(_OUTPUT_CURRENT, '<H')
    _voltage_reg = UnaryStruct(_OP_VOLTAGE, '<H')
    _current_reg = UnaryStruct(_OP_CURRENT, '<H')
    
    _output_voltage_reg = ROUnaryStruct(_OUTPUT_VOLTAGE_1, '<H')
    
    def __init__(self, i2c, address):
        self.i2c_device = I2CDevice(i2c, 0x50 + address)
        self.log = logging.getLogger('cotek')

    '''
    Get manufacturer string
    '''
    @property
    def manufacturer(self) -> str:
        return self._manufacturer_reg.decode().split(',')[0]
    
    '''
    Get model string
    '''
    @property
    def model(self) -> str:
        return self._model_reg.decode().split(',')[0]
    
    '''
    Get revision string
    '''
    @property
    def revision(self) -> str:
        return self._revision_reg.decode()
    
    '''
    Get date of manufacturing in a string time
    '''
    @property
    def date_of_manufacture(self) -> time.struct_time:
        dateStr = self._date_of_manufacture_reg.decode()
        date = datetime.datetime.strptime(dateStr, "%m%d%Y").date()
        return date.timetuple()
    
    '''
    Get the serial number string
    '''
    @property
    def serial(self) -> str:
        return self._serial_reg.decode()
    
    '''
    Get the country of manufacturing
    '''
    @property
    def country(self) -> str:
        return self._country_reg.decode().strip()
    
    '''
    Get the rate output voltage
    '''
    @property
    def rate_output_voltage(self) -> float:
        return self._rate_output_voltage_reg / 100
    
    '''
    Get the rate output current
    '''
    @property
    def rate_output_current(self) -> float:
        return self._rate_output_current_reg / 100
    
    '''
    Get the maximum output voltage
    '''
    @property
    def max_output_voltage(self) -> float:
        return self._max_output_voltage_reg / 100
    
    '''
    Get the maximum output current
    '''
    @property
    def max_output_current(self) -> float:
        return self._max_output_current_reg / 100
    
    '''
    Get the internal temperature
    '''
    @property
    def internal_temp(self) -> int:
        return self._internal_temp_reg
    
    '''
    Get the current voltage from the internal voltmeter
    '''
    @property
    def voltage(self) -> float:
        return self._voltmeter_reg / 100
    
    '''
    Set the voltage
    '''
    @voltage.setter
    def voltage(self, value):
        self._voltage_reg = int(value * 100)
    
    '''
    Get the current current value from the internal ampermeter
    '''
    @property
    def current(self) -> float:
        return self._ammeter_reg / 100
    
    '''
    Set the current
    '''
    @current.setter
    def current(self, value):
        self._current_reg = int(value * 100)
    
    '''
    Get the Over-Voltage-Protection status bit
    True: Overvoltage shutdown
    False: Normal
    '''
    @property
    def OVP_Shutdown(self) -> bool:
        return self._OVP_Shutdown_bit
    
    '''
    Get the Over-Load-Protection status bit
    True: Overload shutdown
    False: Normal
    '''
    @property
    def OLP_Shutdown(self) -> bool:
        return self._OLP_Shutdown_bit
    
    '''
    Get the Over-Temperature-Protection status bit
    True: Internal temperature is over 85 C, Power is shutdown.
    False: Normal Internal temperature.
    '''
    @property
    def OTP_Shutdown(self) -> bool:
        return self._OTP_Shutdown_bit
    
    '''
    Get the FAN status bit
    True: Fan fail, Power is shutdown.
    False: Fan normal working
    '''
    @property
    def FAN_failure(self) -> bool:
        return self._FAN_failure_bit
    
    '''
    Get the Units status bit
    True:  Unit fail, Power is shutdown.
    False: Unit normal working
    '''
    @property
    def AUX_SMPS_Failure(self) -> bool:
        return self._AUX_SMPS_Failure_bit
    
    '''
    Get the High temperature alarm bit
    True: Internal temperature is over 75°C.
    False: Internal temperature normally
    '''
    @property
    def HI_TEMP_Alarm(self) -> bool:
        return self._HI_TEMP_Alarm_bit
    
    '''
    Get the AC Power status bit
    True: AC input < 100 Vac, Output power down.
    False: AC input >= 100 Vac, Normal output
    '''
    @property
    def AC_Input_Power_Down(self) -> bool:
        return self._AC_Input_Power_Down_bit
    
    '''
    Get the AC input status bit
    True: AC input < 85 Vac, Power is off
    False: Normal AC input
    '''
    @property
    def AC_Input_Failure(self) -> bool:
        return self._AC_Input_Failure_bit
    
    '''
    Get the Inhibit by control Signal bit (In Local mode [0x7C.7]=0 only)
    True: Inhibit by VCI, ACI or INHI signal.
    False: Power supply works normal
    '''
    @property 
    def Inhibit_VCI_ACI_INHI(self) -> bool:
        return self._Inhibit_VCI_ACI_INHI_bit
    
    '''
    Get the Inhibit by control Register bit (In Remote mode [0x7C.7]=1 only)
    True: Inhibit by control Register [0x7C.0]
    False: Power supply works normal
    '''
    @property 
    def Inhibit_Control_Register(self) -> bool:
        return self._Inhibit_Control_Register_bit
    
    '''
    Get the power Control mode
    True: output enabled
    False : output disabled
    '''
    @property
    def Power_Control(self) -> bool:
        return self._Power_Control_bit
    
    '''
    Set the power Control mode
    True: output enabled
    False : output disabled
    '''
    @Power_Control.setter
    def Power_Control(self, value):
        self._Power_Control_bit = value

    '''
    Get the command update mode
    True: the command is updated
    False: the command is not updated
    '''
    @property
    def Command_Update(self) -> bool:
        return self._Command_Update_bit
    
    '''
    Set the command update mode
    True: the command is updated
    False: the command is not updated
    '''
    @Command_Update.setter
    def Command_Update(self, value):
        self._Command_Update_bit = value

    '''
    Get the command error status bit
    True: the last command failed
    False: the last command succeeded
    '''
    @property
    def Command_Error(self) -> bool:
        return self._Command_Error_bit
    
    '''
    Get the remote control mode
    True: The remote control is enabled
    False: The remote control is disabled
    '''
    @property
    def Remote_Control(self) -> bool:
        return self._Remote_Control_bit
    
    '''
    Set the remote control mode
    True: The remote control is enabled
    False: The remote control is disabled
    '''
    @Remote_Control.setter
    def Remote_Control(self, value):
        self._Remote_Control_bit = value

    '''
    Log alimentation infos
    '''
    def log_infos(self):
        self.log.info("COTEK INFOS")
        self.log.info(f'{self.manufacturer=}')
        self.log.info(f'{self.model=}')
        self.log.info(f'{self.revision=}')
        self.log.info(f'date_of_manufacture={time.strftime("%d/%m/%Y", self.date_of_manufacture)}')
        self.log.info(f'{self.serial=}')
        self.log.info(f'{self.country=}')
        self.log.info(f'{self.rate_output_voltage=}')
        self.log.info(f'{self.rate_output_current=}')
        self.log.info(f'{self.max_output_voltage=}')
        self.log.info(f'{self.max_output_current=}')
    
    '''
    Log the current command state of the alimentation
    '''
    def log_command_state(self):
        self.log.info('COTEK STATE')
        self.log.info(f'{self.internal_temp=}')
        self.log.info(f'{self.voltage=}')
        self.log.info(f'{self.current=}')
    
    '''
    Log tyhe current status of the alimentation
    '''
    def log_status(self):
        self.log.info('COTEK STATUS')
        self.log.info(f'{self.OVP_Shutdown=}')
        self.log.info(f'{self.OLP_Shutdown=}')
        self.log.info(f'{self.OTP_Shutdown=}')
        self.log.info(f'{self.FAN_failure=}')
        self.log.info(f'{self.AUX_SMPS_Failure=}')
        self.log.info(f'{self.HI_TEMP_Alarm=}')
        self.log.info(f'{self.AC_Input_Power_Down=}')
        self.log.info(f'{self.AC_Input_Failure=}')
        self.log.info(f'{self.Inhibit_VCI_ACI_INHI=}')
        self.log.info(f'{self.Inhibit_Control_Register=}')
        