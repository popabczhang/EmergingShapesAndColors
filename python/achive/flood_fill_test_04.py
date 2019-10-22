# from PIL import Image, ImageDraw
from numpy import *
# from pylab import *
import cv2
# from IPython.display import display
import time
import random
# import ipywidgets as widgets


colorTolerance = 5  #5
s = 20  #space  #10  #100
# picture size: 640x480
nx = 31
ny = 23
textSize = 0.3  #0.05  #0.3

# for less dense grid
s2 = 60
nx2 = 10
ny2 = 8

# black threshold
black = (0,0,0)
dBlack = 200  #400

# flood fill difference
diff = (colorTolerance,colorTolerance,colorTolerance)

# default colors
redRGB = (255,0,0)
greenRGB = (0,255,0)
blueRGB = (0,0,255)
whiteRGB = (255,255,255)
redBGR = (0,0,255)
greenBGR = (0,255,0)
blueBGR = (255,0,0)

# fps
timeLastFrame = 0


# random color function
def RandomComponent():
    return random.randint(0,255)

def RandomColor():
    return (RandomComponent(),RandomComponent(),RandomComponent())

def InitFixedRandomColor(nx,ny):
    colorList = []
    for j in range(ny):
        for i in range(nx):
            colorList.append(RandomColor())
    return colorList

def FixedRandomColor(colorList,i,j,nx,ny):
    return colorList[j*nx+i]

# FPS
def diplay_fps(tLast,img):
    tThis = time.time()
    deltaTime = (tThis - tLast)/1000
    fps = round(1/deltaTime*10)/10
    cv2.putText(img, f'{fps}', (20,20), cv2.FONT_HERSHEY_SIMPLEX, textSize, whiteRGB)
    return tThis

# floodfill webcam
def floodfill_webcam(mirror=False, colorList=[], colorList2=[], tLast=0):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)

        # post processing of each webcam fram
        im = img.copy()
        imbk = im.copy()
        #print(im)
        h,w = im.shape[:2]

        mask = zeros((h+2,w+2), uint8)
        maskbk = mask.copy()

        # loop fill grid - less dense
        for j in range(ny2):
            for i in range(nx2):
                dColor = linalg.norm(imbk[s2*j][s2*i]-black)
                if dColor > dBlack:
                    cv2.floodFill(im,mask,(s2*i,s2*j),FixedRandomColor(colorList2,i,j,nx2,ny2),diff,diff,4 | ( 255 << 8 ))

        # loop fill grid - more dense
        for j in range(ny):
            for i in range(nx):
                #print(f'imbk[s*j][s*i] = {imbk[s*j][s*i]}')
                #print(f'black = {black}')
                dColor = linalg.norm(imbk[s*j][s*i]-black)
                if dColor > dBlack:
                    #print(f's*i = {s*i}; s*j = {s*j}')
                    #print(f'dColor = {dColor}')
                    # reset mask; will be very slow 16+ sec
                    #mask = maskbk.copy()
                    cv2.floodFill(im,mask,(s*i,s*j),FixedRandomColor(colorList,i,j,nx,ny),diff,diff,4 | ( 255 << 8 ))

        # fps
        timeLastFrame = diplay_fps(tLast,im)

        # display
        cv2.imshow('my webcam', im)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit

    cv2.destroyAllWindows()


# main function
def main():
    # fps
    timeLastFrame = time.time()
    # for more dense grid colors
    colorList = InitFixedRandomColor(nx,ny)
    # for less dense grid colors
    colorList2 = InitFixedRandomColor(nx2,ny2)
    # runtime function
    floodfill_webcam(mirror=True, colorList=colorList, colorList2=colorList2, tLast=timeLastFrame)


if __name__ == '__main__':
    main()