import serial

class PelcoD:
    _device = None
    _panSpeed = 0x0
    _tiltSpeed = 0x0

    def __init__(self, port, baudrate=9600, timeout=0):
        self._device=serial.Serial(
            port,
            baudrate,
            timeout=timeout
        )

    def unconnect(self):
        self._device.close()

    def home(self):
        binPacket = self._createPacket(command2=0x49, data1=0x0, data2=0x0)
        self._device.write(binPacket)

    def move(self, x=0, y=0, z=0):
        command2 = 0x0

        # Right
        if x == 1:
            command2 += 0x2
        elif x == -1:
            command2 += 0x4

        if y == 1:
            command2 += 0x10
        elif y == -1:
            command2 += 0x8

        if z == 1 :
            command2 += 0x20
        elif z == -1:
            command2 += 0x40

        binPacket = self._createPacket(command2=command2)
        self._device.write(binPacket)

    def stopMoving(self):
        binPacket = self._createPacket()
        self._device.write(binPacket)

    def setPanSpeed(self, value):
        self._panSpeed = value

    def getPanSpeed(self):
        return self._panSpeed

    def setTiltSpeed(self, value):
        self._tiltSpeed = value

    def getTiltSpeed(self):
        return self._tiltSpeed

    def _createPacket(self, command1 = 0, command2 = 0,
            data1 = None, data2 = None):
        #     
        # Packet bloks:
        # byte 1 - synch byte
        # byte 2 - address
        # byte 3 - command1
        # byte 4 - command2
        # byte 5 - data1
        # byte 6 - data2
        # byte 7 - checksum
        #
        # Bytes 2-6 are Payload Bytes
        #

        if data1 is None:
            data1 = self._panSpeed

        if data2 is None:
            data2 = self._tiltSpeed


        packet = {
            'synch_byte':   0xFF,   # Synch Byte, always FF -   1 byte
            'address':      0x0,    # Address               -   1 byte
            'command1':     0x0,    # Command1              -   1 byte
            'command2':     0x0,    # Command2              -   1 byte
            'data1':        0x0,    # Data1 (PAN SPEED):    -   1 byte
            'data2':        0x0,    # Data2 (TILT SPEED):   -   1 byte 
            'checksum':     0x0     # Checksum:             -   1 byte
        }

        packet['command1'] = command1
        packet['command2'] = command2
            
        packet['data1'] = data1
        packet['data2'] = data2

        # Payload
        payload = packet['address'] + \
            packet['command1'] + packet['command2'] +  \
            packet['data1'] + packet['data2']

        # Checksum
        packet['checksum'] = payload % 256

        binPacket = bytes()
        binPacket += packet['synch_byte'].to_bytes()
        binPacket += packet['address'].to_bytes()
        binPacket += packet['command1'].to_bytes()
        binPacket += packet['command2'].to_bytes()
        binPacket += packet['data1'].to_bytes()
        binPacket += packet['data2'].to_bytes()
        binPacket += packet['checksum'].to_bytes()

        print(packet)
        print(binPacket)

        return binPacket
