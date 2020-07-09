import cv2 as cv
import numpy as np 
from multiprocessing import Process, Value, Array, Queue
from multiprocessing.sharedctypes import Value
import ctypes
import time


# Changeable parameters
maxItr = 500     #maximum amount of iterations per pixel
width = 800       #width in pixels; heigth calculated automatically to keep image proportional
koef = 2        # zooming koeficient. 1 = no zooming, 2 = 2x zoom per mouse button click

def checkSet (c, maxN):
    z = n = 0
    while abs(z) <= 2.0:
        z = z * z + c
        n += 1
        if (n >= maxN):
            return n
    return n

def resize (koef, x = 0, y = 0):
    global xMin, xMax, yMin, yMax
    global xLen, yLen
    global w, h
    global wSS, hSS

    xNewCenter = xMin + x * wSS
    yNewCenter = yMin + y * hSS

    xLen = xLen*koef
    yLen = yLen*koef

    xMin = xNewCenter - xLen/2
    xMax = xNewCenter + xLen/2
    yMin = yNewCenter - yLen/2
    yMax = yNewCenter + yLen/2

    wSS = xLen/w       #width step size
    hSS = yLen/h       #height step size

def mouseEvent (event, x, y, flags, param):
    global h, w, maxItr
    global wSS, hSS
    global xMin, yMin
    if event == cv.EVENT_LBUTTONDOWN:
        resize(koef, x, y)
        main(h, w, maxItr, wSS, hSS, xMin, yMin)

def countImgValues(minH, maxH, w, arr, wSS, hSS, xMin, yMin):
    # check if complex number c belongs to mandelbrot set
    for i in range (minH, maxH):   #i is for rows so works on vertical (y) axis, hence decides imaginary part
        li = []
        for j in range (0, w):     #j is for colums so works on horizonatal (x) axis, hence decides real part
            ci = i*hSS + yMin
            cr = j*wSS + xMin  
            c = complex(cr, ci)
            itrCount = checkSet (c, maxItr) 
            itrCount +=1           # for smoother coloring
            arr[i*w + j] = itrCount

def main(h, w, maxItr, wSS, hSS, xMin, yMin):
    
    processes = []
    img = np.zeros((h, w), dtype = np.uint8)         #For max iteration values for each pixel
    imgRGB = np.zeros((h, w, 3), dtype = np.uint8)   #RGB values fir each pixel
    mArr = Array("I", h*w)                           #Thread-safe array for multiprocessing

    tic = time.perf_counter()                        # Start counting time after arrays initalization

    processes.append(Process(target = countImgValues, args = (int(h*0/1), int(h*1/1), w, mArr, wSS, hSS, xMin, yMin)))

    # processes.append(Process(target = countImgValues, args = (int(h*0/1), int(h*1/2), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*1/2), int(h*2/2), w, mArr, wSS, hSS, xMin, yMin)))

    # processes.append(Process(target = countImgValues, args = (int(h*0/4), int(h*1/4), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*1/4), int(h*2/4), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*2/4), int(h*3/4), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*3/4), int(h*4/4), w, mArr, wSS, hSS, xMin, yMin)))

    # 4 processes with improven load share
    # processes.append(Process(target = countImgValues, args = (int(h*0/8), int(h*3/8), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*3/8), int(h*4/8), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*4/8), int(h*5/8), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*5/8), int(h*8/8), w, mArr, wSS, hSS, xMin, yMin)))

    # processes.append(Process(target = countImgValues, args = (int(h*0/6), int(h*1/6), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*1/6), int(h*2/6), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*2/6), int(h*3/6), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*3/6), int(h*4/6), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*4/6), int(h*5/6), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*5/6), int(h*6/6), w, mArr, wSS, hSS, xMin, yMin)))

    # processes.append(Process(target = countImgValues, args = (int(h*0/8), int(h*1/8), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*1/8), int(h*2/8), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*2/8), int(h*3/8), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*3/8), int(h*4/8), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*4/8), int(h*5/8), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*5/8), int(h*6/8), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*6/8), int(h*7/8), w, mArr, wSS, hSS, xMin, yMin)))
    # processes.append(Process(target = countImgValues, args = (int(h*7/8), int(h*8/8), w, mArr, wSS, hSS, xMin, yMin)))

    print("Processes created")


    for proc in processes:
        proc.start()
    print("Processes started")

    for proc in processes:
        proc.join()    
    print("Processes joined")

    for i in range (h):         #i is for rows so works on vertical (y) axis, hence decides imaginary part
        for j in range (w):     #j is for colums so works on horizonatal (x) axis, hence decides real part
            if (mArr[i * w + j] >= maxItr):
                imgRGB[i, j] = (0, 0, 0)
            else:
                imgRGB[i, j, 0] = round(255 - mArr[i * w + j] * 255 / maxItr * 0.5)
                imgRGB[i, j, 1] = round(255 - mArr[i * w + j] * 255 / maxItr * 0.7)
                imgRGB[i, j, 2] = round(255 - mArr[i * w + j] * 255 / maxItr * 1)

    toc = time.perf_counter()      # Stop counting time
    print("Time parallel:          %12.4f" % (toc-tic))

    cv.imshow("Mandelbrot", imgRGB)
    cv.waitKey(10)

    cv.setMouseCallback("Mandelbrot", mouseEvent)
    cv.imwrite("Mandelbrot.png", imgRGB) 
    cv.waitKey(0)
    cv.destroyWindow("Mandelbrot")




#initializing 


xMin, xMax = -2.01, 1  #min and max values of x axis (real part of complex number)
yMin, yMax = -1.25, 1.25  #min and max values of y axis (imaginary part of complex number)

xLen = xMax - xMin #width length in terms of complex plane
yLen = yMax - yMin #height length in terms of complex plane

w = width
h = round(w*yLen/xLen)

wSS = xLen/w       #width step size
hSS = yLen/h       #height step size

koef = 1/koef

if __name__ == '__main__':

    main(h, w, maxItr, wSS, hSS, xMin, yMin)





    