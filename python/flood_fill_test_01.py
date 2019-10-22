from PIL import Image
from numpy import *
from pylab import *

import cv2

# read image
filename = 'pic1.jpg'
im = cv2.imread(filename)
h,w = im.shape[:2]

# flood fill example
diff = (2,2,2)
mask = zeros((h+2,w+2), uint8)
#cv2.floodFill(im,mask,(10,10),(0,0,255),diff,diff)

for i in range(200):
    for j in range(200):
        cv2.floodFill(im,mask,(5*i,5*j),(0,255,0),diff,diff)


# show the result in a OpenCV window
cv2.imshow('Flood Fill Image', im)
cv2.waitKey(0)
cv2.destroyAllWindows()

# save the result
cv2.imwrite('pic1_result.jpg', im)