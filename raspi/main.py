import cv2
import pygame
from picamera2 import Picamera2
from image_processing.poo_image import ImageProcessor
from lidar_sensor.poo_lidar import LidarSensor
from haptic.poo_haptic import VibrationController
import time

pygame.init()
pygame.mixer.init()

# sound_success = pygame.mixer.Sound("raspi/son/success.wav")  # Son pour les croix
# sound_error = pygame.mixer.Sound("raspi/son/error.wav")      # Son pour les cercles
# sound_warning = pygame.mixer.Sound("raspi/son/warning.wav")  # Son pour les cartons proches

croix_a_droite = pygame.mixer.Sound("raspi/son/croix_a_droite.wav")
croix_a_gauche = pygame.mixer.Sound("raspi/son/croix_a_gauche.wav")
croix_au_centre = pygame.mixer.Sound("raspi/son/croix_au_millieu.wav")
carre_au_centre = pygame.mixer.Sound("raspi/son/carre_au_millieu.wav")
carre_a_droite = pygame.mixer.Sound("raspi/son/carre_a_droite.wav")
carre_a_gauche = pygame.mixer.Sound("raspi/son/carre_a_gauche.wav")
carton_devant = pygame.mixer.Sound("raspi/son/carton_devant.wav")

processor = ImageProcessor()
lidar = LidarSensor()

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1920, 1080)
picam2.preview_configuration.main.format = 'XBGR8888'
picam2.video_configuration.controls.FrameRate = 25.0
picam2.start()

LOWER_SCREEN_RATIO = 0.3  #detect object only on the lower part of the screen
DISTANCE_THRESHOLD = 1.0  #critical distance for cardboard (in meters)


vibration_controller = VibrationController(left_sensor_pin=27, right_sensor_pin=17)

try:
    while True:
        frame_wrong_color = picam2.capture_array()
        frame = cv2.cvtColor(frame_wrong_color, cv2.COLOR_RGB2BGR)
        resized_frame = cv2.resize(frame, (1280, 720))

        hsv = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)

        lower_white = (0, 0, 200)
        upper_white = (180, 40, 255)
        mask_white = cv2.inRange(hsv, lower_white, upper_white)

        lower_red = (0, 120, 70) 
        upper_red = (10, 255, 255) 
        lower_red2 = (170, 120, 70)
        upper_red2 = (180, 255, 255)
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)
        edges_red = cv2.Canny(red_mask, 50, 150)

        lower_brown = (10, 50, 50)
        upper_brown = (30, 255, 200)
        mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
        contours_brown, _ = cv2.findContours(mask_brown, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        squares = processor.detect_square(mask_white, resized_frame)
        crosses = processor.detect_cross(mask_white, resized_frame)
        intersection = processor.detect_red_line(edges_red, resized_frame)
        cardboards = processor.detect_cardboard(contours_brown, resized_frame)

        if intersection:
            x_coord = int(intersection[0])
            tolerance = 100
            if x_coord > 700:
                vibration_controller.vibrate_right()
                # print("Droite")
            elif x_coord < 400:
                vibration_controller.vibrate_left()
                # print("Gauche")
            # else:
            #     print("OK")

        played_square_sound = False
        played_cross_sound = False
        played_cardboard_sound = False
        height = resized_frame.shape[0]
        lower_screen_threshold = int(height * (1 - LOWER_SCREEN_RATIO))
        lower_screen_threshold_cardboard = 400

        for square in squares:
            if square[0][0][1] > lower_screen_threshold and not played_square_sound:
                x_coord = int(square[0][0][0])
                if x_coord > resized_frame.shape[1] / 2 + 50:
                    carre_a_droite.play()
                elif x_coord < resized_frame.shape[1] / 2 - 50:
                    carre_a_gauche.play()
                else:
                    carre_au_centre.play()
                played_square_sound = True

        for cross in crosses:
            if cross[0][0][1] > lower_screen_threshold and not played_cross_sound:
                x_coord = int(cross[0][0][0])
                if x_coord > resized_frame.shape[1] / 2 + 50:
                    croix_a_droite.play()
                elif x_coord < resized_frame.shape[1] / 2 - 50:
                    croix_a_gauche.play()
                else:
                    croix_au_centre.play()
                played_cross_sound = True


        for cardboard in cardboards:
            x, y, w, h = cardboard
            if w > h and not played_cardboard_sound:
                
                #add this part if you want to use the lidar sensor
                # distance = lidar.read_distance()
                # if distance and distance < DISTANCE_THRESHOLD:
                #    sound_warning.play()
                #     break
                
                if y > lower_screen_threshold_cardboard:
                    carton_devant.play()
                    played_cardboard_sound = True



        #add this part if you want to display the processed frame
        # cv2.imshow('Processed Frame', resized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Programme interrompu par l'utilisateur.")

finally:
    picam2.stop()
    lidar.close()
    cv2.destroyAllWindows()
    pygame.quit()