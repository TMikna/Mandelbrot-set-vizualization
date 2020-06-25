import cv2 as cv
import numpy as np 

maxItr = 1000
width = 400       #width, heigth calculated automatically


def checkSet (c, maxN):
    z = n = 0
    while abs(z) <= 2:
        z = z * z + c
        n += 1
        if (n >= maxN):
            return n
    return n


xMin, xMax = -2, 1  #min and max values of x axis (real part of complex number)
yMin, yMax = -1.25, 1.25  #min and max values of y axis (imaginary part of complex number)

xLen = xMax - xMin #width length in terms of complex plane
yLen = yMax - yMin #height length in terms of complex plane

w = width
h = round(w*yLen/xLen)

wSS = xLen/w       #width step size
hSS = yLen/h       #height step size

img = np.zeros((h, w), dtype = np.uint8)

# check if complex number c belongs to mandelbrot set
for i in range (0, h):         #i is for rows so works on vertical (y) axis, hence decides imaginary part
    for j in range (0, w):     #j is for colums so works on horizonatal (x) axis, hence decides real part
        ci = i*hSS + yMin
        cr = j*wSS + xMin  
        c = complex(cr, ci)
        itrCount = checkSet (c, maxItr) 
        # if (itrCount == maxItr):
        #     img[i, j] = 0
        # else:
        img[i, j] = round(255 - itrCount * 255 / maxItr)
    cv.imshow("Mandelbrot", img)
    cv.waitKey(10)

cv.waitKey(0)
cv.destroyWindow("Mandelbrot")