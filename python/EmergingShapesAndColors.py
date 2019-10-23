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
nx2 = 11
ny2 = 8

# black threshold
black = (0,0,0)
white = (255,255,255)
dBlack = 200  #400
dBlackSample = 200
dWhiteSample = 150

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
timeThisFrame = 0


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

# color from sample image
def InitSampleColor(nx,ny):
    colorList = []
    # read color sample image
    filename = 'pic5.jpg'
    imColorSample = cv2.imread(filename)
    h,w = imColorSample.shape[:2]
    for j in range(ny):
        for i in range(nx):
            isColorful = False
            while(isColorful==False):
                sampleColor = imColorSample[random.randint(10,h-11)][random.randint(10,w-11)]
                #print(sampleColor)
                dColorBlack = linalg.norm(sampleColor-black)
                dColorWhite = linalg.norm(white-sampleColor)
                if dColorBlack > dBlackSample and dColorWhite > dWhiteSample:
                    sampleColor = (int(sampleColor[0]),int(sampleColor[1]),int(sampleColor[2]))
                    colorList.append(sampleColor)
                    isColorful = True
    return colorList

# FPS
def diplay_fps(img):
    global timeThisFrame
    global timeLastFrame
    timeThisFrame = time.time()
    deltaTime = timeThisFrame - timeLastFrame
    fps = round(1/deltaTime*10)/10
    cv2.putText(img, f'{fps}', (10,10), cv2.FONT_HERSHEY_SIMPLEX, textSize, whiteRGB)
    timeLastFrame = timeThisFrame

# floodfill webcam
def floodfill_webcam(mirror, colorList, colorList2):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)

        # post processing of each webcam fram
        im = img.copy()
        imbk = im.copy()
        h,w = im.shape[:2]

        mask = zeros((h+2,w+2), uint8)
        maskbk = mask.copy()

        # loop fill grid - less dense
        for j in range(ny2):
            for i in range(nx2):
                dColor = linalg.norm(imbk[s2*j][s2*i]-black)
                if dColor > dBlack:
                    cv2.floodFill(im,mask,(int(s2*i+s2/2),int(s2*j+s2/2)),FixedRandomColor(colorList2,i,j,nx2,ny2),diff,diff,4 | ( 255 << 8 ))

        # loop fill grid - more dense
        for j in range(ny):
            for i in range(nx):
                dColor = linalg.norm(imbk[s*j][s*i]-black)
                if dColor > dBlack:
                    cv2.floodFill(im,mask,(s*i,s*j),FixedRandomColor(colorList,i,j,nx,ny),diff,diff,4 | ( 255 << 8 ))

        # show color palette
        for j in range(ny2):
            for i in range(nx2):
                t = ny2*j+i
                if t < len(colorList2):
                    cv2.circle(im, (int(s2*i+s2/2),int(s2*j+s2/2)), 3, colorList2[t], 5)

        # fps
        diplay_fps(im)

        # display
        cv2.imshow('my webcam', im)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit

        # fps control
        #time.sleep(0.1)

    cv2.destroyAllWindows()


# main function
def main():
    # fps
    timeLastFrame = time.time()
    # color list
    colorListRandom = InitFixedRandomColor(nx,ny)  # for more dense grid
    colorListRandom2 = InitFixedRandomColor(nx2,ny2)  # for less dense grid
    colorListSample = InitSampleColor(nx,ny)  # for more dense grid
    colorListSample2 = InitSampleColor(nx2,ny2)  # for less dense grid
    # runtime function
    floodfill_webcam(True, colorListSample, colorListSample2)


# initiation
if __name__ == '__main__':
    main()