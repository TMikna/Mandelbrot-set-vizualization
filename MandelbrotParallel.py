import cv2 as cv
import numpy as np 
from multiprocessing import Process, Value, Array, Queue
from multiprocessing.sharedctypes import Value
import ctypes

maxItr = 100
width = 100       #width, heigth calculated automatically


def checkSet (c, maxN):
    z = n = 0
    while abs(z) <= 2.5:
        z = z * z + c
        n += 1
        if (n >= maxN):
            return n
    return n

def paintImg():
    global hSS, wSS, yMin, xMin
    global maxItr
    img = np.zeros((h, w, 3), dtype = np.uint8)
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

            itrCount +=2

            if (itrCount >= maxItr):
                img[i, j] = (0, 0, 0)
            else:
                img[i, j, 0] = round(255 - itrCount * 255 / maxItr)
                img[i, j, 1] = round(255 - itrCount * 255 / maxItr * 0.25)
                img[i, j, 2] = round(255 - itrCount * 255 / maxItr * 0.9)
# some coloring: https://stackoverflow.com/questions/16500656/which-color-gradient-is-used-to-color-mandelbrot-in-wikipedia
            # if (itrCount < maxItr and itrCount > maxItr* 0.8):
            #     img[i, j] = [255, 255, 255]
        if(i%10 == 0):    
            cv.imshow("Mandelbrot", img)
            cv.waitKey(10)

def resize (koef, x = 0, y = 0):
    global xMin, xMax, yMin, yMax
    global xLen, yLen
    global w, h
    global wSS, hSS

    # x and y dictance from image center
    xC = x-w/2
    yC = y-h/2

    xMinOld = xMin
    xMaxOld = xMax
    yMinOld = yMin
    yMaxOld = yMax

    # xMin = xMin*koef + xC*wSS
    # xMax = xMax*koef + xC*wSS
    # yMin = yMin*koef + yC*hSS
    # yMax = yMax*koef + yC*hSS

    xMin = xMin*koef
    xMax = xMax*koef
    yMin = yMin*koef
    yMax = yMax*koef

    xLen = xMax - xMin #width length in terms of complex plane
    yLen = yMax - yMin #height length in terms of complex plane

    xMin = xMin + xC*wSS
    xMax = xMax + xC*wSS
    yMin = yMin + yC*hSS
    yMax = yMax + yC*hSS

    wSS = xLen/w       #width step size
    hSS = yLen/h       #height step size

def mouseEvent (event, x, y, flags, param):

    if event == cv.EVENT_LBUTTONDOWN:
        resize(0.5, x, y)
        print("down")
        print(f"{x}; {y}")
        paintImg()

#from sequential with zooming
###########################################################ę
# new methods
def queueToList(q):
    listt = []
    while q.qsize() > 0:
        listt.append(q.get())
    return listt

def countImgValues(minH, maxH, minW, maxW, q):
    # check if complex number c belongs to mandelbrot set
    print("Cunction started")
    for i in range (minH, maxH):         #i is for rows so works on vertical (y) axis, hence decides imaginary part
        li = []
        for j in range (minW, maxW):     #j is for colums so works on horizonatal (x) axis, hence decides real part
            ci = i*hSS + yMin
            cr = j*wSS + xMin  
            c = complex(cr, ci)
            itrCount = checkSet (c, maxItr) 
            # if (itrCount == maxItr):
            #     img[i, j] = 0
            # else:

            itrCount +=1

            li.append(itrCount)
        q.put(li)
    print("Cunction finished")
            # if (itrCount >= maxItr):
            #     img[i, j] = (0, 0, 0)
            # else:
            #     img[i, j, 0] = round(255 - itrCount * 255 / maxItr)
            #     img[i, j, 1] = round(255 - itrCount * 255 / maxItr * 0.25)
            #     img[i, j, 2] = round(255 - itrCount * 255 / maxItr * 0.9)






xMin, xMax = -2.01, 1  #min and max values of x axis (real part of complex number)
yMin, yMax = -1.25, 1.25  #min and max values of y axis (imaginary part of complex number)

xLen = xMax - xMin #width length in terms of complex plane
yLen = yMax - yMin #height length in terms of complex plane

w = width
h = round(w*yLen/xLen)

wSS = xLen/w       #width step size
hSS = yLen/h       #height step size

img = np.zeros((h, w), dtype = np.uint8)

mArr = Array("I", (h,w))

q1 = Queue()
q2 = Queue()
q3 = Queue()
q4 = Queue()

processes = []
if __name__ == '__main__':

    # processes.append(Process(target = countImgValues, args = (int(h*0/4), int(h*4/4), 0, w, q1)))
    # processes.append(Process(target = countImgValues, args = (int(h*1/4), int(h*2/4), 0, w, q2)))
    # processes.append(Process(target = countImgValues, args = (int(h*2/4), int(h*3/4), 0, w, q3)))
    # processes.append(Process(target = countImgValues, args = (int(h*3/4), int(h*4/4), 0, w, q4)))

    print("Processes created")

    for proc in processes:
        proc.start()

    print("Processes started")


    for proc in processes:
        proc.join()


    print("Processes joined")


    # countImgValues(int(h*0/2), int(h*1/2), 0, w, q1)
    # countImgValues(int(h*1/2), int(h*2/2), 0, w, q2)

    print("Here")

    li1 = []
    while q1.qsize() > 0:
        li1.append(q1.get())
        
    li2 = queueToList(q2)
    li3 = queueToList(q3)
    li4 = queueToList(q4)
    li = [*li1, *li2, *li3, *li4]
    img = np.array(li).reshape((h,w))
    print(img)
    # paintImg()

    imgRGB = np.zeros((h, w, 3), dtype = np.uint8)

    for i in range (h):         #i is for rows so works on vertical (y) axis, hence decides imaginary part
        for j in range (w):     #j is for colums so works on horizonatal (x) axis, hence decides real part
            if (img[i, j] >= maxItr):
                imgRGB[i, j] = (0, 0, 0)
            else:
                imgRGB[i, j, 0] = round(255 - img[i, j] * 255 / maxItr)
                imgRGB[i, j, 1] = round(255 - img[i, j] * 255 / maxItr * 0.25)
                imgRGB[i, j, 2] = round(255 - img[i, j] * 255 / maxItr * 0.9)

    cv.imshow("Mandelbrot", imgRGB)
    cv.waitKey(10)
    cv.imwrite("mand.png", imgRGB) 
    # cv.setMouseCallback("Mandelbrot", mouseEvent)
    cv.waitKey(0)
    cv.destroyWindow("Mandelbrot")