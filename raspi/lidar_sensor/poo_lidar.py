import sys

if sys.platform.startswith('linux'):
    import serial
    serial_available = True
else:
    serial_available = False
    print("Serial communication not available on this platform. Simulation mode enabled.")

class LidarSensor:
    def __init__(self, port='/dev/serial0', baudrate=115200, timeout=0):
        self.serial_available = serial_available
        if self.serial_available:
            self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        else:
            self.ser = None

    def read_distance(self):
        if not self.serial_available:
            print("Simulating LiDAR reading.")
            return 1.23

        try:
            counter = self.ser.in_waiting
            if counter > 8:
                bytes_serial = self.ser.read(9)
                self.ser.reset_input_buffer()

                if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                    distance = bytes_serial[2] + bytes_serial[3] * 256
                    return distance / 100
        except Exception as e:
            print(f"Read error in LiDAR : {e}")
        return None

    def close(self):
        if self.serial_available:
            self.ser.close()
