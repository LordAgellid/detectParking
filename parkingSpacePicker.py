import cv2 as cv 
import numpy as np 
import pickle

path = './images/parking_lot_1.png' 

width, height = 60, 70 

try:
    with open("carParkPos", 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def mouseClick(events, x,y,flags, params):
    if events == cv.EVENT_LBUTTONDOWN:
        posList.append((x,y)) 
    
    if events == cv.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1, y1 = pos
            if x1-(width//2)<x<x1+width and y1-(height//2)<y<y1+height:
                posList.pop(i)
    with open("carParkPos", 'wb') as f:
        pickle.dump(posList, f)
    

while True:
    img = cv.imread(path)
    
    for pos in posList:
        x = pos[0]
        y = pos[1]
        cv.rectangle(img, (x-(width//2),y-(height//2)), (x+(width//2),y+(height//2)), (255,0,255), 2)
        
    
    cv.imshow('image', img)
    
    cv.setMouseCallback('image', mouseClick)
    
    if cv.waitKey(1) & 0xFF ==ord('q'):
        break    

