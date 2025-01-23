import cv2 as cv

#specifying the file path and initialize the video object
path = 'second simulation.mp4'
vid = cv.VideoCapture(path)

#running a while loop so that all the frames of the video object are read repeatedly
while True:
    
    #A condition that stops the video after the last frame is read.
    isTrue, frame = vid.read()
    if not isTrue:
        break

    #Displaying the video
    cv.imshow('frame',frame)
    
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

#When 'd' is pressed above, the video is closed and the last frame is written as a jpg file
vid.release()
cv.imwrite('screenshot3.jpg',frame)
