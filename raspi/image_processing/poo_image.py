import cv2
import numpy as np

class ImageProcessor:
    """Class for processing images and detecting different objects."""
    def __init__(self, min_contour_area=500):
        """
        Initialize the image processor.
        
        :param min_contour_area: Minimum area for contours to be considered valid.
        """
        self.min_contour_area = min_contour_area

    @staticmethod
    def average_intersection(lines):
        """
        Calculate the average intersection point of multiple lines.

        :param lines: List of line equations (slope, intercept).
        :return: Average intersection point (x, y) or None if no intersection.
        """
        intersections = []
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                m1, b1 = lines[i]
                m2, b2 = lines[j]
                if m1 != m2: # Ensure lines are not parallel
                    x_inter = (b2 - b1) / (m1 - m2) # Find x intersection
                    y_inter = m1 * x_inter + b1 # Find y intersection
                    intersections.append((x_inter, y_inter))

        if not intersections:
            return None
        
        # Calculate the average intersection point
        x_avg = sum([x for x, y in intersections]) / len(intersections)
        y_avg = sum([y for x, y in intersections]) / len(intersections)
        return (x_avg, y_avg)

    def detect_red_line(self, edges, image):
        """
        Detects red lines using the Hough Transform and finds their intersection.

        :param edges: Edge-detected image.
        :param image: Original image for visualization (optional).
        :return: Average intersection point of red lines or None if no lines found.
        """
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=30, maxLineGap=10)
        line_equations = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if x2 != x1: # Avoid division by zero
                    m = (y2 - y1) / (x2 - x1) # Calculate slope
                    b = y1 - m * x1 # Calculate intercept
                    line_equations.append((m, b)) 
                    #Uncomment the line below to draw detected lines
                    # cv2.line(image, (0, int(b)), (image.shape[1], int(m * image.shape[1] + b)), (0, 255, 0), 2)
            return self.average_intersection(line_equations)
        return None

    def detect_square(self, mask, image):
        """
        Detects squares in a given binary mask.

        :param mask: Binary mask image where squares are white.
        :param image: Original image for visualization (optional).
        :return: List of detected squares (contours).
        """
        edged = cv2.Canny(mask, 30, 200) # Detect edges
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

                if area > min_contour_area and len(approx) == 4: # Check if the contour has 4 sides
                    aspect_ratio = float(w) / h
                    if 0.8 <= aspect_ratio <= 1.3: # Ensure it's roughly a square
                        # Uncomment the lines below to draw detected squares
                        # cv2.drawContours(image, [approx], -1, (255, 0, 0), 2)
                        # cv2.putText(image, "Square", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                        detected_squares.append(approx)
        return detected_squares

    def detect_cross(self, mask_white, image):
        """
        Detects cross shapes in a given binary mask.

        :param mask_white: Binary mask where crosses are white.
        :param image: Original image for visualization (optional).
        :return: List of detected crosses (contours).
        """
        mask = cv2.GaussianBlur(mask_white, (5, 5), 0) # Apply Gaussian blur to reduce noise
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detected_crosses = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100: # Ignore small noise
                approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
                if len(approx) == 12:  # Approximate number of edges for a cross
                    detected_crosses.append(approx)
                    # Uncomment the line below to draw detected crosses
                    # cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
        return detected_crosses

    def detect_cardboard(self, contours_brown, image):
        """
        Detects brown cardboard objects based on contours.

        :param contours_brown: List of contours detected in the brown color range.
        :param image: Original image for visualization (optional).
        :return: List of detected cardboards as (x, y, width, height).
        """
        detected_cardboards = []
        for contour_brown in contours_brown:
            area = cv2.contourArea(contour_brown)
            if area > 1000: # Ignore small objects
                x, y, w, h = cv2.boundingRect(contour_brown) # Get bounding box
                if w > h: # Ensure the object is wider than tall (likely a cardboard)
                    detected_cardboards.append((x, y, w, h))
                    # Uncomment the line below to draw detected cardboards
                    # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        return detected_cardboards
