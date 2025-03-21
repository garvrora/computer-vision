import cv2 as cv
import numpy as np

img = cv.imread(r"D:\workspace\python programs\openCV\application\fruit detection\given_img.jpeg")
roi = img.copy()
    
points1 = np.array([[0,247],[335,277],[355,292],[335,306],[240,303],[0,341]],dtype=np.int32)
points1 = points1.reshape((-1, 1, 2))

points2 = np.array([[1168,183],[839,195],[780,222],[808,251],[991,260],[1168,309]],dtype = np.int32)
points2 = points2.reshape((-1, 1, 2))
    
cv.polylines(roi,[points1],isClosed = True, color = (0,0,0),thickness = 2)
cv.fillPoly(roi,[points1],color = (0,0,0))

cv.polylines(roi,[points2],isClosed = True, color = (0,0,0),thickness = 2)
cv.fillPoly(roi,[points2],color = (0,0,0))

hsv = cv.cvtColor(roi,cv.COLOR_BGR2HSV)


lower = np.array([112,129,0])
upper = np.array([179,255,255])

mask = cv.inRange(hsv,lower,upper)
mask = cv.dilate(mask,(3,3), iterations = 5)
    
contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
filtered_contours = [cont for cont in contours if cv.contourArea(cont) > 15]


count = 0
for contour in filtered_contours:
    count += 1 
    x, y, w, h = cv.boundingRect(contour)
    cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv.putText(img,f'FRUIT {count}',(x-w-40,y+h+20),cv.FONT_HERSHEY_TRIPLEX,0.6,(0,255,0),thickness = 2)
    
cv.imshow('detected fruits',img)
       



# remove static unwanted regions from roi
# convert bgr to hsv
# create upper and lower limits for masks
# dilate the mask
# use bitwise_and to implement the mask
# use contour detection and filter out the small contours using area thresholding
# draw rectangles wherever contours are detected and put text

# NOTE: manual work is required to calculate the area threshold, dilation iterations, and the lower numpy array for mask. the given values
# were finalized after picking the best case scenario by adjusting trackbars and monitoring the image manipulation changes in real time. creating polygons
# to cover the propellers were also located on the image using trackbars
