import cv2 as cv 
import cvzone 
import pickle
import numpy as np 

with open("carParkPos", 'rb') as f:
    posList = pickle.load(f)

path = './videos/parking_lot_1.mp4' 
cap = cv.VideoCapture(path)

width, height = 40, 50 


def preProcessing(img):
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5,5), 1)
    imgTreshHold = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16) 
    imgMedian = cv.medianBlur(imgTreshHold, 3)
    kernel = np.ones((3,3), np.int8)
    imgDilate = cv.dilate(imgMedian, kernel, iterations=1 )
    return imgDilate    


def checkParkinSpaces(imgProcess):
    for pos in posList:
        x = pos[0]
        y = pos[1]
        
        imgCropped = imgProcess[y-(height//2):y+(height//2), x-(width//2):x+(width//2)]
        imgResize = cv.resize(imgCropped, (imgCropped.shape[0]*2,imgCropped.shape[1]*2))
        
        count = cv.countNonZero(imgCropped)
        cvzone.putTextRect(img, str(count), (x-(width//2), y+(height//2)-10), scale=1, thickness=1, offset=0)
        
        if count>300 :
            color = (0,0,255)
            cv.rectangle(img, (x-(width//2),y-(height//2)), (x+(width//2),y+(height//2)), color, 2)
            print('une personne est lah')
        else:
            color = (0,255,0)
            cv.rectangle(img, (x-(width//2),y-(height//2)), (x+(width//2),y+(height//2)), color, 2)
            print('personne est lah')
            
        
        cv.imshow(str(x*y), imgResize)
        
        
        

while True:
    success, img = cap.read()
    imgDilate = preProcessing(img)
    
    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
    
    checkParkinSpaces(imgDilate)
    
    for pos in posList:
        x = pos[0]
        y = pos[1]
        # cv.rectangle(img, (x-(width//2),y-(height//2)), (x+(width//2),y+(height//2)), (255,0,255), 2)
        # cv.rectangle(imgDilate, (x-(width//2),y-(height//2)), (x+(width//2),y+(height//2)), (255,0,255), 2)
        
    # cv.imshow('Parking', img)
    # cv.imshow('Parking2', imgDilate)
            
    if cv.waitKey(1) & 0xFF ==ord('q'):
        break    

