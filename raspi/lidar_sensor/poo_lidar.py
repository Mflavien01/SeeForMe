import sys

# Check if the script is running on a Linux system (Raspberry Pi)
if sys.platform.startswith('linux'):
    import serial # Import serial communication library for Raspberry Pi
    serial_available = True # Serial communication is available
else:
    serial_available = False # Serial communication is not available
    print("Serial communication not available on this platform. Simulation mode enabled.")

class LidarSensor:
    """Class for handling LiDAR sensor readings."""

    def __init__(self, port='/dev/serial0', baudrate=115200, timeout=0):
        """
        Initialize the LiDAR sensor.

        :param port: Serial port where the LiDAR is connected.
        :param baudrate: Communication speed (default 115200 baud).
        :param timeout: Timeout for serial communication (default 0).
        """
        self.serial_available = serial_available # Check if serial is available
        if self.serial_available:
            self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        else:
            self.ser = None # No real serial connection (simulation mode)

    def read_distance(self):
        """
        Read distance from the LiDAR sensor.

        :return: Distance in meters or None if an error occurs.
        """
        if not self.serial_available:
            print("Simulating LiDAR reading.") # Fake distance for testing
            return 1.23 # Example simulated value

        try:
            counter = self.ser.in_waiting # Check available bytes in the serial buffer
            if counter > 8: # Ensure enough data is available
                bytes_serial = self.ser.read(9) # Read 9 bytes of data
                self.ser.reset_input_buffer() # Clear the buffer
                
                # Check if data starts with the expected header bytes (0x59 0x59)
                if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                    distance = bytes_serial[2] + bytes_serial[3] * 256 # Compute distance
                    return distance / 100 # Convert from cm to meters
        except Exception as e:
            print(f"Read error in LiDAR : {e}") # Print error message
        return None # Return None if reading fails

    def close(self):
        """Close the serial connection to the LiDAR sensor."""
        if self.serial_available:
            self.ser.close()
