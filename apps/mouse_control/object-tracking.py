import cv2
import numpy as np
import uinput

def nothing(x):
    pass

class Mouse_control:
    def __init__(self):
        self.device = uinput.Device([
                 uinput.BTN_LEFT,
                 uinput.BTN_RIGHT,
                 uinput.REL_X,
                 uinput.REL_Y,
                 ])

    def move(self, dx, dy):
        self.device.emit(uinput.REL_X, dx, syn=False)
        self.device.emit(uinput.REL_Y, dy)

if __name__ == '__main__':
    mouse = Mouse_control()
    cap = cv2.VideoCapture(1)
    kernel = np.ones((5,5),np.uint8)
    
    cv2.namedWindow('frame')
    
    dx = 0
    dy = 0
    cxn = 0
    cyn = 0
    cxp = 0
    cyp = 0
    # define range of blue color in HSV
    lower_green = np.array([100,140,23])
    upper_green = np.array([128,255,255])
    
    while(1):
    
        # Captura un frame
        _, frame = cap.read()
    
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        
    
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_green, upper_green)    
        
        maskd = cv2.medianBlur(mask,11)
        #maskd = cv2.dilate(maskd,kernel,iterations = 1) #1
        maskd = cv2.morphologyEx(maskd, cv2.MORPH_GRADIENT, kernel) # 6
    
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= maskd)

        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        cv2.imshow('maskd',maskd)
    
        moments = cv2.moments(maskd)
        area = moments['m00']
        if (area != 0):
            cxn = int(moments['m10']/area)
            cyn = int(moments['m01']/area)        
            if (cxp != cxn):
                dx = cxn - cxp
                cxp = cxn
            if (cyp != cyn):
                dy = cyn - cyp
                cyp = cyn
            # print dx, dy
            mouse.move(-dx,dy)

        #cv2.imshow('res',res)
        k = cv2.waitKey(100) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
