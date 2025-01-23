import cv2 as cv
import numpy as np
import time

#A function that is called for creating trackbars
def nothing(x):
    pass


#A timer that shows time elapsed after the eruption in hours, minutes, and seconds
def clock(clk):
    m, s = divmod(clk, 60)
    h, m = divmod(m, 60)
    return(int(s),int(m) ,int(h))

#Creating GUI for trackbars
cv.namedWindow('CIRCLE')
cv.resizeWindow('CIRCLE',300,300)

cv.createTrackbar('MoveX','CIRCLE',400,1200,nothing)
cv.createTrackbar('MoveY','CIRCLE',0,720,nothing)

#Initialising the radius (r) of the sound wave, the starting time (t0) and the speed (301.667 m/s)
r = 0
speed = 1086 / 3600
t0 = time.time()

while True:

    #The frame is freezed in which the explosive wave radius would keep on increasing until 'd' is pressed
    #t1 is the time of beginning of a while loop iteration
    t1 = time.time()
    img = cv.imread('closeup1000kmis143p.png')
    x = cv.getTrackbarPos('MoveX','CIRCLE')
    y = cv.getTrackbarPos('MoveY','CIRCLE')

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

    #Distance  = ( speed )( elapsed time )
    dist = speed * (t1 - t0)
    r_final = int(r)

    #The centre of the eruption is specified and the circle representing the sound wave is drawn on the image with other elements
    centre = (638,283)
    cv.circle(img,centre,r_final,(0,255,255),thickness = 2)
    cv.line(img,(centre[0]+r_final,centre[1]),(centre[0]+r_final-20,centre[1]-16),(0,255,255),thickness = 1)
    cv.line(img,(centre[0]+r_final,centre[1]),(centre[0]+r_final-20,centre[1]+16),(0,255,255),thickness = 1)
    cv.line(img,(centre[0]+r_final,centre[1]),(centre[0]+r_final,centre[1]),(0,255,255),thickness = 1)
    cv.line(img,centre,(centre[0]+r_final,centre[1]),(0,255,255),thickness = 1)
    cv.putText(img,f'{int(dist)}KM',(centre[0]+10,centre[1]-10),cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,255), thickness = 1)
    
    #Point of explosion marked on the map
    cv.putText(img,'POINT OF EXPLOSION',(centre[0]-145,centre[1]+145),cv.FONT_HERSHEY_TRIPLEX,0.8,(255,255,255), thickness = 2)
    cv.line(img,(centre[0]-5,centre[1]+5),(centre[0]-140,centre[1]+140),(255,255,255),thickness = 2)

    #Various other locations pointed on the map for reference
    cv.putText(img,'JAKARTA',(671+145,287-105),cv.FONT_HERSHEY_TRIPLEX,0.8,(255,255,255), thickness = 2)
    cv.line(img,(671,287),(671+140,287-100),(255,255,255),thickness = 2)

    cv.putText(img,'PERTH',(806,700),cv.FONT_HERSHEY_TRIPLEX,0.8,(255,255,255), thickness = 2)
    cv.putText(img,'VELLORE',(269,30),cv.FONT_HERSHEY_TRIPLEX,0.8,(255,255,255), thickness = 2)
    cv.putText(img,'MANIPAL',(140,50),cv.FONT_HERSHEY_TRIPLEX,0.8,(255,255,255), thickness = 2)
    cv.putText(img,'SINGAPORE',(620,166),cv.FONT_HERSHEY_TRIPLEX,0.8,(255,255,255), thickness = 2)

    #Text at the edge of the circle that indicates it as a sound wave travelling at 1086km/h
    cv.putText(img,'KABOOM!',(r_final+10+centre[0],centre[1]),cv.FONT_HERSHEY_TRIPLEX, 0.7, (0,255,255), thickness = 2)
    cv.putText(img,'(1086KM/H)',(r_final+10+centre[0],centre[1]+30),cv.FONT_HERSHEY_TRIPLEX, 0.7, (0,255,255), thickness = 1)

    #The time elapsed after eruption
    cv.putText(img,f'Time after eruption:',(720,530),cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,0), thickness = 2)
    cv.putText(img,f'{clock(t1 - t0)[2]} hours',(720,570),cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,0), thickness = 2)
    cv.putText(img,f'{clock(t1 - t0)[1]} minutes',(720,610),cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,0), thickness = 2)
    cv.putText(img,f'{clock(t1 - t0)[0]} seconds',(720,650),cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,0), thickness = 2)

    #showing the output
    cv.imshow('window',img)
    print(r)

    #Increment of radius such that r increases by 0.043 pixels per second, equivalent to 301.667 meters per second
    r += 0.0431383
    t2 = time.time()

    #The while loop executes faster than 1 second.
    #to ensure timely execution within 1 second, a delay is added which makes each iteration 1 second long only.
    delta = t2 - t1
    if delta < 1:
        time.sleep(1 - delta)
   
cv.destroyAllWindows()

