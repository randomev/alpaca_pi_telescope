
from threading import Timer
from threading import Lock
from logging import Logger
import serial
from config import Config

class TelescopeDevice:
    """Simulated rotator device that does moves in separate Timer threads.

    Properties and  methods generally follow the Alpaca interface.
    Debug tracing here via (commented out) print() to avoid locking issues.
    Hopefully you are familiar with Python threading and the need to lock
    shared data items.

    **Mechanical vs Virtual Position**

    In this code 'mech' refers to the raw mechanical position. Note the
    conversions ``_pos_to_mech()`` and ``_mech_to_pos()``. This is where
    the ``Sync()`` offset is applied.

    """
    #
    # Only override __init_()  and run() (pydoc 17.1.2)
    #
    def __init__(self, logger: Logger, config: Config):
        self._lock = Lock()
        self.name: str = 'device'
        self.logger = logger
        #
        # Rotator device constants
        #
        self._can_reverse: bool = True
        self._step_size: float = 1.0
        self._steps_per_sec: int = 6
        #
        # Rotator device state variables
        #
        self._reverse = False
        self._mech_pos = 0.0
        self._tgt_mech_pos = 0.0
        self._pos_offset = 0.0      # TODO In real life this must be persisted
        self._is_moving = False
        #self._connected = False
        #
        # Rotator engine
        #
        self._timer: Timer = None
        self._interval: float = 1.0 / self._steps_per_sec
        self._stopped: bool = True
        self.serial_port = None

    def is_connected(self): # -> bool:

        if self.serial_port == None:
            self._is_connected = False
        else:
            try:
                # Try to write to the port. If this fails, an exception will be raised.
                self.serial_port.write(b'')
                self._is_connected = True
            except serial.SerialException:
                # If writing to the port failed, it's not open.
                self._is_connected = False

        return self._is_connected

    def connect(self, conn: bool):
        if conn:
            # Replace '/dev/ttyS1' with your serial port and 9600 with your baud rate
            self.serial_port = serial.Serial(Config.serial_port, 9600)
        else:
            if self.serial_port != None: 
                if self.serial_port.is_open:
                    self.serial_port.close()

        if self.serial_port == None:
            self._is_connected = False
        else:
            if self.serial_port.is_open:
                self._is_connected = True
            else:
                self._is_connected = False

        self.logger.info(f'Connected: {self._is_connected} Serial Port: {self.serial_port}')
    
    def pulse_guide(self, direction: int, duration: int):
        command = f'#PG_{direction};{duration}\n'
        self.serial_port.write(command.encode())
    
    def is_slewing(self):
        self.serial_port.reset_input_buffer()  # Clear the input buffer
        command = f'#SL_0;0\n'
        self.serial_port.write(command.encode())
        reply = self.serial_port.readline().decode().strip().capitalize()
        print(reply)
        if reply == 'True':
            self._is_moving = True
        else:
            self._is_moving = False

        return self._is_moving
        # Read and decode the reply
            
    # @property
    # def connected(self) -> bool:
    #     self._lock.acquire()
    #     res = self._connected
    #     self._lock.release()
    #     return res
 
    # @connected.setter
    # def connected (self, connected: bool):
    #     self._lock.acquire()
    #     if (not connected) and self._connected and self._is_moving:
    #         self._lock.release()
    #         # Yes you could call Halt() but this is for illustration
    #         raise RuntimeError('Cannot disconnect while rotator is moving')
    #     self._connected = connected
    #     self._lock.release()
    #     if connected:
    #         self.logger.info('[connected]')
    #     else:
    #         self.logger.info('[disconnected]')
