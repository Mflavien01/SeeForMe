import cv2
import pygame
from picamera2 import Picamera2
from image_processing.poo_image import ImageProcessor
from lidar_sensor.poo_lidar import LidarSensor
from haptic.poo_haptic import VibrationController
import time

# Initialize pygame for sound playback
pygame.init()
pygame.mixer.init()

# Load sound files for different detections
croix_a_droite = pygame.mixer.Sound("raspi/son/croix_a_droite.wav")
croix_a_gauche = pygame.mixer.Sound("raspi/son/croix_a_gauche.wav")
croix_au_centre = pygame.mixer.Sound("raspi/son/croix_au_millieu.wav")
carre_au_centre = pygame.mixer.Sound("raspi/son/carre_au_millieu.wav")
carre_a_droite = pygame.mixer.Sound("raspi/son/carre_a_droite.wav")
carre_a_gauche = pygame.mixer.Sound("raspi/son/carre_a_gauche.wav")
carton_devant = pygame.mixer.Sound("raspi/son/carton_devant.wav")

# Initialize the image processor and lidar sensor
processor = ImageProcessor()
lidar = LidarSensor()

# Initialize and configure the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1920, 1080)
picam2.preview_configuration.main.format = 'XBGR8888'
picam2.video_configuration.controls.FrameRate = 25.0
picam2.start()


# Constants for processing
LOWER_SCREEN_RATIO = 0.3  # Defines the bottom part of the screen to focus on
DISTANCE_THRESHOLD = 1.0 # Distance limit for object detection (in meters)

# Initialize the vibration controller for haptic feedback
vibration_controller = VibrationController(left_sensor_pin=27, right_sensor_pin=17)

try:
    while True:
        # Capture an image from the camera
        frame_wrong_color = picam2.capture_array()
        frame = cv2.cvtColor(frame_wrong_color, cv2.COLOR_RGB2BGR)
        resized_frame = cv2.resize(frame, (1280, 720))

        # Convert to HSV color space for color detection
        hsv = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)

        # Define color ranges for white, red, and brown detection
        lower_white = (0, 0, 200)
        upper_white = (180, 40, 255)
        mask_white = cv2.inRange(hsv, lower_white, upper_white)   # Detect white shapes

        lower_red = (0, 120, 70) 
        upper_red = (10, 255, 255) 
        lower_red2 = (170, 120, 70)
        upper_red2 = (180, 255, 255)
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2) # Combine red masks
        edges_red = cv2.Canny(red_mask, 50, 150) # Detect red edges (lines)

        lower_brown = (10, 50, 50)
        upper_brown = (30, 255, 200)
        mask_brown = cv2.inRange(hsv, lower_brown, upper_brown) # Detect brown objects
        contours_brown, _ = cv2.findContours(mask_brown, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Detect different objects in the frame
        squares = processor.detect_square(mask_white, resized_frame)
        crosses = processor.detect_cross(mask_white, resized_frame)
        intersection = processor.detect_red_line(edges_red, resized_frame)
        cardboards = processor.detect_cardboard(contours_brown, resized_frame)

        # Detect red line intersections for navigation
        if intersection:
            x_coord = int(intersection[0])
            tolerance = 100
            if x_coord > 700:
                vibration_controller.vibrate_right() # Vibrate right if red line is on the right
            elif x_coord < 400:
                vibration_controller.vibrate_left() # Vibrate left if red line is on the left

        played_sound = False # Ensure only one sound is played at a time
        height = resized_frame.shape[0]
        lower_screen_threshold = int(height * (1 - LOWER_SCREEN_RATIO)) # Define lower screen area
        lower_screen_threshold_cardboard = 400 # Specific threshold for cardboards

        # Detect squares and play corresponding sounds
        for square in squares:
            if square[0][0][1] > lower_screen_threshold and not played_sound:
                x_coord = int(square[0][0][0])
                if x_coord > resized_frame.shape[1] / 2 + 50:
                    carre_a_droite.play() # Square on the right
                elif x_coord < resized_frame.shape[1] / 2 - 50:
                    carre_a_gauche.play() # Square on the left
                else:
                    carre_au_centre.play() # Square in the center
                played_sound = True

        # Detect crosses and play corresponding sounds
        for cross in crosses:
            if cross[0][0][1] > lower_screen_threshold and not played_sound:
                x_coord = int(cross[0][0][0])
                if x_coord > resized_frame.shape[1] / 2 + 50:
                    croix_a_droite.play() # Cross on the right
                elif x_coord < resized_frame.shape[1] / 2 - 50:
                    croix_a_gauche.play() # Cross on the left
                else:
                    croix_au_centre.play() # Cross in the center
                played_sound = True

        # Detect cardboards and play a warning sound
        for cardboard in cardboards:
            x, y, w, h = cardboard
            if w > h and not played_sound: # Only process wide objects (cardboards)

                # Uncomment the lines below to use the lidar sensor for distance checking
                # distance = lidar.read_distance()
                # if distance and distance < DISTANCE_THRESHOLD:
                #    sound_warning.play()
                #     break
                
                if y > lower_screen_threshold_cardboard :
                    carton_devant.play() # Play warning sound for cardboard
                    played_sound = True



        # Uncomment the lines below to display the processed frame
        # cv2.imshow('Processed Frame', resized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): # Press 'q' to exit the loop
            break

except KeyboardInterrupt:
    print("Programme interrompu par l'utilisateur.") # Handle keyboard interruption

finally:
    # Cleanup resources before exiting
    picam2.stop()
    lidar.close()
    cv2.destroyAllWindows()
    pygame.quit()
