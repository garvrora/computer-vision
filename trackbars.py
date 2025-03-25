import cv2 as cv
import numpy as np
from math import *

class Trackbar:

    colors = {
        "red": (0, 0, 255),
        "green": (0, 255, 0),
        "blue": (255, 0, 0),
        "yellow": (0, 255, 255),
        "cyan": (255, 255, 0),
        "purple": (255, 0, 255),
        "white": (255, 255, 255),
        "black": (0, 0, 0)
    }
    
    def __init__(self, source, mode, n_sides=3, window_name='Trackbar', window_size=(500, 500)):
        self.mode = mode
        self.window_name = window_name
        self.window_size = window_size
        self.n_sides = n_sides
        self.is_video = isinstance(source, cv.VideoCapture)

        if self.is_video:
            self.video = source
            isTrue, frame = self.video.read()
            self.image = frame
        else:
            self.image = source

        self.hsv = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)
        cv.namedWindow(self.window_name)
        cv.resizeWindow(self.window_name, self.window_size[0], self.window_size[1])
        self._build_trackbars()

    def _nothing(self, x):
        return x

    def _create_rect_trackbar(self):
        parameters = {
            "MoveX": self.image.shape[1],
            "MoveY": self.image.shape[0],
            "Width": self.image.shape[1],
            "Height": self.image.shape[0]
        }
        
        for parameter, limit in parameters.items():
            cv.createTrackbar(parameter, self.window_name, 0, limit, self._nothing)

    def _create_circle_trackbar(self):
        parameters = {
            'MoveX': self.image.shape[1],
            'MoveY': self.image.shape[0],
            'Radius': self.image.shape[0]
        }

        for parameter, limit in parameters.items():
            cv.createTrackbar(parameter, self.window_name, 0, limit, self._nothing)

    def _create_hsv_mask_trackbar(self):
        parameters = {
            'H1': 180,
            'S1': 255,
            'V1': 255,
            'H2': 180,
            'S2': 255,
            'V2': 255,
            'Dilations': 100,
            'Erosions': 100
        }

        for parameter, limit in parameters.items():
            cv.createTrackbar(parameter, self.window_name, 0, limit, self._nothing)

    def _create_polygon_trackbar(self):
        for i in range(self.n_sides):
            cv.createTrackbar(f"X{i+1}", self.window_name, 0, self.image.shape[1], self._nothing)
            cv.createTrackbar(f"Y{i+1}", self.window_name, 0, self.image.shape[0], self._nothing)

    def _build_trackbars(self):
        match self.mode:
            case "rectangle":
                self._create_rect_trackbar()
            case "circle":
                self._create_circle_trackbar()
            case "polygon":
                self._create_polygon_trackbar()
            case "hsv":
                self._create_hsv_mask_trackbar()
            case _:
                raise ValueError("Wrong mode selected.")

    def get(self, showArea=True, showDim=True, showCoord=True, shapeColor='green', textColor='green', shapeThickness=2, textThickness=2, textSize=0.5):
        if self.is_video:
            isTrue, frame = self.video.read()
            if not isTrue:
                self.video.set(cv.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.video.read()
                
            self.image = frame
            self.hsv = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)

        copy = self.image.copy()

        match self.mode:
            case "rectangle":
                return self._get_rect_trackbar(copy, showArea, showDim, showCoord, shapeColor, textColor, shapeThickness, textThickness, textSize)
            case "circle":
                return self._get_circle_trackbar(copy, showArea, showDim, showCoord, shapeColor, textColor, shapeThickness, textThickness, textSize)
            case "polygon":
                return self._get_polygon_trackbar(copy, showDim, showCoord, shapeColor, textColor, shapeThickness, textThickness, textSize)
            case "hsv":
                return self._get_hsv_trackbar(copy)
            case _:
                raise ValueError("Wrong mode selected.")

    def _get_rect_trackbar(self, image, showArea, showDim, showCoord, shapeColor, textColor, shapeThickness, textThickness, textSize):
        x = cv.getTrackbarPos('MoveX', self.window_name)
        y = cv.getTrackbarPos('MoveY', self.window_name)
        w = cv.getTrackbarPos('Width', self.window_name)
        h = cv.getTrackbarPos('Height', self.window_name)
        
        cv.rectangle(image, (x,y), (x+w,y+h), color = Trackbar.colors[shapeColor], thickness = shapeThickness)
        if showCoord:
            cv.putText(image, f'({x},{y})',(x-50,y-35),cv.FONT_HERSHEY_SIMPLEX, textSize, Trackbar.colors[textColor], thickness=textThickness)
        if showDim:
            cv.putText(image, f'{w}',((x+x+w)//2,y-5),cv.FONT_HERSHEY_SIMPLEX, textSize, Trackbar.colors[textColor], thickness=textThickness)
            cv.putText(image, f'{h}',((x+w+5),(y+y+h)//2),cv.FONT_HERSHEY_SIMPLEX, textSize, Trackbar.colors[textColor], thickness=textThickness)
        if showArea:
            cv.putText(image, f'{w*h}',(x-50,y+h+35),cv.FONT_HERSHEY_SIMPLEX, textSize, Trackbar.colors[textColor], thickness=textThickness)
        return image
            
    def _get_circle_trackbar(self, image, showArea, showDim, showCoord, shapeColor, textColor, shapeThickness, textThickness, textSize):
        x = cv.getTrackbarPos('MoveX', self.window_name)
        y = cv.getTrackbarPos('MoveY', self.window_name)
        r = cv.getTrackbarPos('Radius', self.window_name)
        centre = (x,y)

        cv.circle(image, centre, r, Trackbar.colors[shapeColor],thickness = shapeThickness)
        if showCoord:
            cv.putText(image, f'({x},{y})', (x,y), cv.FONT_HERSHEY_SIMPLEX, textSize, Trackbar.colors[textColor], thickness=textThickness)
        if showDim:
            cv.putText(image, f'{r}', (x+30,y-r-5), cv.FONT_HERSHEY_SIMPLEX, textSize, Trackbar.colors[textColor], thickness=textThickness)
        if showArea:
            cv.putText(image, f'{int(pi*r*r)}', (x+r+5,y), cv.FONT_HERSHEY_SIMPLEX, textSize, Trackbar.colors[textColor], thickness=textThickness)
        return image
           
    def _poly_distance(self, points, i, j):
        pi, pj = points[i], points[j]
        return np.linalg.norm(pi - pj)
        
    def _get_polygon_trackbar(self, image, showDim, showCoord, shapeColor, textColor, shapeThickness, textThickness, textSize):    
        points = np.array([[cv.getTrackbarPos(f'X{i}', self.window_name), cv.getTrackbarPos(f'Y{i}', self.window_name)]
                             for i in range(1, self.n_sides + 1)], dtype=np.int32)
        
        cv.polylines(image, [points], isClosed = True, color = Trackbar.colors[shapeColor], thickness = shapeThickness)
        if showCoord:
            for i in range(1,self.n_sides+1):
                cv.putText(image, f'(x{i},y{i})', points[i-1], cv.FONT_HERSHEY_SIMPLEX, textSize, Trackbar.colors[textColor], thickness=textThickness)

        if showDim:
            distances = []
            for i in range(self.n_sides):
                dist = self._poly_distance(points, i, (i+1)%(self.n_sides))
                distances.append(dist)
            for i in range(0, self.n_sides):
                midpoint = ((points[i][0] + points[(i + 1) % self.n_sides][0]) // 2, 
                        (points[i][1] + points[(i + 1) % self.n_sides][1]) // 2)
                cv.putText(image, f'{int(distances[i])}', midpoint, cv.FONT_HERSHEY_SIMPLEX, textSize, Trackbar.colors[textColor], thickness=textThickness)
        return image

    def _get_hsv_trackbar(self, image):
        H1 = cv.getTrackbarPos('H1', self.window_name)
        S1 = cv.getTrackbarPos('S1', self.window_name)
        V1 = cv.getTrackbarPos('V1', self.window_name)
        H2 = cv.getTrackbarPos('H2', self.window_name)
        S2 = cv.getTrackbarPos('S2', self.window_name)
        V2 = cv.getTrackbarPos('V2', self.window_name)
        i = cv.getTrackbarPos('Dilations', self.window_name)
        j = cv.getTrackbarPos('Erosions', self.window_name)

        lower = np.array([H1, S1, V1])
        upper = np.array([H2, S2, V2])

        mask = cv.inRange(self.hsv, lower, upper)
        mask = cv.dilate(mask, (3, 3), iterations=i)
        mask = cv.erode(mask, (3, 3), iterations=j)
        result = cv.bitwise_and(image, image, mask=mask)
        return result
