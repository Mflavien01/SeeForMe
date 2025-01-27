import cv2
import numpy as np

class ImageProcessor:
    def __init__(self, min_contour_area=500):
        self.min_contour_area = min_contour_area

    @staticmethod
    def average_intersection(lines):
        intersections = []
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                m1, b1 = lines[i]
                m2, b2 = lines[j]
                if m1 != m2:
                    x_inter = (b2 - b1) / (m1 - m2)
                    y_inter = m1 * x_inter + b1
                    intersections.append((x_inter, y_inter))

        if not intersections:
            return None

        x_avg = sum([x for x, y in intersections]) / len(intersections)
        y_avg = sum([y for x, y in intersections]) / len(intersections)
        return (x_avg, y_avg)

    def detect_red_line(self, edges, image):
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=30, maxLineGap=10)
        line_equations = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if x2 != x1:
                    m = (y2 - y1) / (x2 - x1)
                    b = y1 - m * x1
                    line_equations.append((m, b))
                    # cv2.line(image, (0, int(b)), (image.shape[1], int(m * image.shape[1] + b)), (0, 255, 0), 2)
            return self.average_intersection(line_equations)
        return None

    def detect_square(self, mask, image):
        edged = cv2.Canny(mask, 30, 200)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        min_contour_area = 500 
        detected_squares = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            M = cv2.moments(contour)

            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                area = cv2.contourArea(contour)
                x, y, w, h = cv2.boundingRect(contour)

                if area > min_contour_area and len(approx) == 4:
                    aspect_ratio = float(w) / h
                    if 0.8 <= aspect_ratio <= 1.3:
                        # cv2.drawContours(image, [approx], -1, (255, 0, 0), 2)
                        # cv2.putText(image, "Square", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                        detected_squares.append(approx)
        return detected_squares

    def detect_cross(self, mask_white, image):
        mask = cv2.GaussianBlur(mask_white, (5, 5), 0)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detected_crosses = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:
                approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
                if len(approx) == 12:
                    detected_crosses.append(approx)
                    # cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
        return detected_crosses

    def detect_cardboard(self, contours_brown, image):
        detected_cardboards = []
        for contour_brown in contours_brown:
            area = cv2.contourArea(contour_brown)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(contour_brown)
                if w > h:
                    detected_cardboards.append((x, y, w, h))
                    # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        return detected_cardboards
