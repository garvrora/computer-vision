import cv2 as cv
import numpy as np
import time

#A timer that shows time elapsed after the eruption in hours, minutes, and seconds
def clock(clk):
    m, s = divmod(clk, 60)
    h, m = divmod(m, 60)
    return(int(s),int(m) ,int(h))

#A function that is called for creating trackbars
def nothing(x):
    pass

#Creating GUI for trackbars
cv.namedWindow('CIRCLE')
cv.resizeWindow('CIRCLE',300,300)

cv.createTrackbar('MoveX','CIRCLE',400,1200,nothing)
cv.createTrackbar('MoveY','CIRCLE',0,720,nothing)
cv.createTrackbar('Rad','CIRCLE',0,720,nothing)

#Initialising the radius (r) of the sound wave, the starting time (timer0) and the speed (301.667 m/s)
r = 0
timer0 = int(time.time())
speed = 1086 / 3600

while True:
    
    #The frame is freezed in which the explosive wave radius would keep on increasing until 'd' is pressed
    #timer1 is the time a while loop iteration begins
    timer1 = int(time.time())

    #Distance  = ( speed )( elapsed time )
    dist = speed * (timer1 - timer0)
    img = cv.imread('closeup10kmis107p.png')

    x = cv.getTrackbarPos('MoveX','CIRCLE')
    y = cv.getTrackbarPos('MoveY','CIRCLE')

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

    #The centre of the eruption is specified and the circle representing the sound wave is drawn on the image with other elements
    centre = (483,368)
    cv.circle(img,centre,int(r),(0,255,255),thickness = 5)
    cv.line(img,(centre[0]+int(r),centre[1]),(centre[0]+int(r)-20,centre[1]-16),(0,255,255),thickness = 2)
    cv.line(img,(centre[0]+int(r),centre[1]),(centre[0]+int(r)-20,centre[1]+16),(0,255,255),thickness = 2)
    cv.line(img,(centre[0]+int(r),centre[1]),(centre[0]+int(r),centre[1]),(0,255,255),thickness = 2)
    cv.line(img,centre,(centre[0]+int(r),centre[1]),(0,255,255),thickness = 2)

    
    cv.putText(img,f'{int(dist)}KM',(centre[0]+10,centre[1]-10),cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,255), thickness = 2)

    #Ouskirsts of Jakarta near the volcano pointed on the map for reference
    cv.putText(img,'OUTSKIRTS',(1066,247),cv.FONT_HERSHEY_TRIPLEX, 1, (255,255,255), thickness = 2)
    cv.putText(img,'OF',(1066,277),cv.FONT_HERSHEY_TRIPLEX, 1, (255,255,255), thickness = 2)
    cv.putText(img,'JAKARTA',(1066,307),cv.FONT_HERSHEY_TRIPLEX, 1, (255,255,255), thickness = 2)

    #Text at the edge of the circle that indicates it as a sound wave travelling at 1086km/h
    cv.putText(img,'KABOOM!',(int(r)+493,368),cv.FONT_HERSHEY_TRIPLEX, 0.7, (0,255,255), thickness = 2)
    cv.putText(img,'(1086KM/H)',(int(r)+493,398),cv.FONT_HERSHEY_TRIPLEX, 0.7, (0,255,255), thickness = 1)

    #The time elapsed after eruption
    cv.putText(img,'Time after eruption:',(600,610),cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,0), thickness = 2)
    cv.putText(img,f'{clock(timer1-timer0)[0]} seconds',(600,640),cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,0), thickness = 2)
    cv.putText(img,f'{clock(timer1-timer0)[1]} minutes',(600,670),cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,0), thickness = 2)

    cv.line(img,(centre[0],200),(centre[0]+567,200),(0,255,0),thickness = 2)
    cv.line(img,(centre[0],200),(centre[0]+20,180),(0,255,0),thickness = 2)
    cv.line(img,(centre[0],200),(centre[0]+20,220),(0,255,0),thickness = 2)
    cv.line(img,(centre[0]+567,200),(centre[0]+547,180),(0,255,0),thickness = 2)
    cv.line(img,(centre[0]+567,200),(centre[0]+547,220),(0,255,0),thickness = 2)
    cv.putText(img,'53KM',((centre[0]+567//2),170),cv.FONT_HERSHEY_TRIPLEX, 0.7, (0,255,0), thickness = 2)
    
    #showing the output
    cv.imshow('window',img)

    #Increment of radius such that r increases by 0.043 pixels per second, equivalent to 301.667 meters per second
    r += 3.22783
    t2 = time.time()

    delta = t2 - timer1

    #The while loop executes faster than 1 second.
    #to ensure timely execution within 1 second, a delay is added which makes each iteration 1 second long only.    
    if delta != 1:
        time.sleep(1 - delta)

cv.destroyAllWindows()
