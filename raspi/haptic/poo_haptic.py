import sys
import time

if sys.platform.startswith('linux'):
    import RPi.GPIO as GPIO
    gpio_available = True
else:
    gpio_available = False
    print("GPIO not available on this platform. Simulation mode enabled.")

class VibrationController:
    def __init__(self, left_sensor_pin, right_sensor_pin):
        self.left_sensor_pin = left_sensor_pin
        self.right_sensor_pin = right_sensor_pin
        self.gpio_available = gpio_available

        if self.gpio_available:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.left_sensor_pin, GPIO.OUT)
            GPIO.setup(self.right_sensor_pin, GPIO.OUT)

    def vibrate_left(self, duration=1):
        self._vibrate(self.left_sensor_pin, duration)

    def vibrate_right(self, duration=1):
        self._vibrate(self.right_sensor_pin, duration)

    def vibrate_both(self, duration=1):
        self._vibrate(self.left_sensor_pin, duration)
        self._vibrate(self.right_sensor_pin, duration)

    def _vibrate(self, pin, duration):
        if self.gpio_available:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(duration)
            GPIO.output(pin, GPIO.LOW)
        else:
            print(f"Simulating vibration on pin {pin} for {duration} seconds.")

    def cleanup(self):
        if self.gpio_available:
            GPIO.cleanup()

    def stop_vibration(self):
        if self.gpio_available:
            GPIO.output(self.left_sensor_pin, GPIO.LOW)
            GPIO.output(self.right_sensor_pin, GPIO.LOW)
