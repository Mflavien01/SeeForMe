import sys
import time

# Check if the script is running on a Raspberry Pi (Linux-based OS)
if sys.platform.startswith('linux'):
    import RPi.GPIO as GPIO # Import GPIO library for Raspberry Pi
    gpio_available = True # GPIO is available
else:
    gpio_available = False # GPIO is not available (e.g., on Windows/Mac)
    print("GPIO not available on this platform. Simulation mode enabled.")

class VibrationController:
    """Class to control vibration motors using Raspberry Pi GPIO pins."""
    def __init__(self, left_sensor_pin, right_sensor_pin):
        """
        Initialize the vibration controller.
        
        :param left_sensor_pin: GPIO pin for the left vibration motor
        :param right_sensor_pin: GPIO pin for the right vibration motor
        """
        self.left_sensor_pin = left_sensor_pin
        self.right_sensor_pin = right_sensor_pin
        self.gpio_available = gpio_available # Check if GPIO is available

        if self.gpio_available:
            # Set up GPIO pins for output
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.left_sensor_pin, GPIO.OUT)
            GPIO.setup(self.right_sensor_pin, GPIO.OUT)

    def vibrate_left(self, duration=1):
        """Trigger the left vibration motor for a specified duration (default 1 second)."""
        self._vibrate(self.left_sensor_pin, duration)

    def vibrate_right(self, duration=1):
        """Trigger the right vibration motor for a specified duration (default 1 second)."""
        self._vibrate(self.right_sensor_pin, duration)

    def vibrate_both(self, duration=1):
        """Trigger both left and right vibration motors simultaneously."""
        self._vibrate(self.left_sensor_pin, duration)
        self._vibrate(self.right_sensor_pin, duration)

    def _vibrate(self, pin, duration):
        """Internal method to handle vibration logic."""
        if self.gpio_available:
            GPIO.output(pin, GPIO.HIGH) # Turn on vibration motor
            time.sleep(duration) # Keep vibrating for the given duration
            GPIO.output(pin, GPIO.LOW)  # Turn off vibration motor
        else:
            print(f"Simulating vibration on pin {pin} for {duration} seconds.") # Simulation mode

    def cleanup(self):
        """Clean up GPIO settings when the program exits."""
        if self.gpio_available:
            GPIO.cleanup()

    def stop_vibration(self):
        """Stop all vibration motors immediately."""
        if self.gpio_available:
            GPIO.output(self.left_sensor_pin, GPIO.LOW)
            GPIO.output(self.right_sensor_pin, GPIO.LOW)
