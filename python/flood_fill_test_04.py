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
textSize = 0.2  #0.05  #0.3

s2 = 60
# picture size: 640x480
nx2 = 10
ny2 = 8

black = (0,0,0)
dBlack = 200  #400

redRGB = (255,0,0)
greenRGB = (0,255,0)
blueRGB = (0,0,255)
redBGR = (0,0,255)
greenBGR = (0,255,0)
blueBGR = (255,0,0)

# # read image
# #filename = r'C:\Users\RYAN\Dropbox (MIT)\01_Work\MAS\18_Fall 2019\191020_flood_fill_test\pic2.jpg'
# filename = 'pic4_3_1080p.jpg'
# im = cv2.imread(filename)
# imbk = cv2.imread(filename)
# #print(im)
# h,w = im.shape[:2]
# pil_im = Image.fromarray(im)
# display(pil_im)

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

# flood fill example
diff = (colorTolerance,colorTolerance,colorTolerance)

# loop fill grid
# msec1 = int(round(time.time() * 1000))
# for j in range(ny):
#     for i in range(nx):
#         #out.clear_output()
#         # mark testing pixel to red
#         #print(f'imbk[s*j][s*i] = {imbk[s*j][s*i]}')
#         #print(f'black = {black}')
#         dColor = linalg.norm(imbk[s*j][s*i]-black)
#         if dColor > dBlack:
#             #print(f's*i = {s*i}; s*j = {s*j}')
#             #print(f'dColor = {dColor}')
#             # reset mask; will be very slow 16+ sec
#             #mask = maskbk.copy()
#             cv2.floodFill(im,mask,(s*i,s*j),RandomColor(),diff,diff,4 | ( 255 << 8 ))
#             # display each step
#             #pil_im = Image.fromarray(im)
#             #display(pil_im)
#             #time.sleep(3)
# msec2 = int(round(time.time() * 1000))
# print(f'{msec2-msec1} milliseconds passed for all flood fill operations')

# # put texts
# for j in range(ny):
#     for i in range(nx):
#         dColor = linalg.norm(imbk[s*j][s*i]-black)
#         if dColor > dBlack:
#             # paint the pixel blue
#             #im[s*j][s*i] = blue
#             # put blue text
#             cv2.putText(im, f'{s*i},{s*j}', (s*i,s*j), cv2.FONT_HERSHEY_SIMPLEX, textSize, blueRGB)
#         else:
#             # put red text
#             cv2.putText(im, f'{s*i},{s*j}', (s*i,s*j), cv2.FONT_HERSHEY_SIMPLEX, textSize, redRGB)



# show the result in a OpenCV window
#cv2.imshow('Flood Fill Image', im)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# save the result
#cv2.imwrite('pic4_result.jpg', im)

# # display the saved ima
# pil_im = Image.fromarray(im)
# display(pil_im)


# # display the mask
# pil_msk = Image.fromarray(mask)
# display(pil_msk)


def show_webcam(mirror=False, colorList=[], colorList2=[]):
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

        # display
        cv2.imshow('my webcam', im)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    colorList = InitFixedRandomColor(nx,ny)
    colorList2 = InitFixedRandomColor(nx2,ny2)
    #print(colorList)
    show_webcam(mirror=True, colorList=colorList, colorList2=colorList2)


if __name__ == '__main__':
    main()