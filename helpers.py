from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab
from math import log, e
from statistics import mean
import cv2
import numpy as np
from objects import *

'''
This file contains all the helper functions that might be called in the
animation framework.
As you can infer from the long import list, these helpers are in fact the 
core of the app, including feature detection with opencv and linear regression.
'''

#inspired by #https://www.google.com/imgres?imgurl=https://i.stack.imgur.com/XrUW3.gif&imgrefurl=https://stackoverflow.com/questions/27465157/drawing-basic-shapes-in-python-2&docid=bXljnN1NbJm-MM&tbnid=UAOGIQ4B58Q-5M:&vet=1&w=520&h=643&source=sh/x/im
def fakeTransparentRect(canvas,x1, y1, x2, y2):
    for i in range(x1,x2,2):
        canvas.create_line(i,y1,i,y2,fill='gray81')
    for i in range(y1,y2,3):
        canvas.create_line(x1,i,x2,i,fill='white')
    canvas.create_rectangle(x1, y1, x2, y2,width=3,outline='white')

def fitWindow(filemane):
    image=Image.open(filemane)
    img=ImageTk.PhotoImage(image)
    w,h=img.width(),img.height()
    ratio=w/h
    if ratio>(1100/700):
        w=1100
        h=int(1100/ratio)
    else:
        h=700
        w=int(700*ratio)
    return image.resize((w,h),Image.ANTIALIAS)

#adapted from https://pythonspot.com/tk-file-dialogs/
def loadImage(data):
    data.img=filedialog.askopenfilename(initialdir="/",title="Load your image")
    if data.img:
        data.actualImage=ImageTk.PhotoImage(fitWindow(data.img))

#adapted from
#https://stackoverflow.com/questions/41940945/saving-canvas-from-tkinter-to-file    
def save(data):
    result=ImageGrab.grab().crop((150,50,950,700))
    file=filedialog.asksaveasfilename(filetypes=[('image','*.png')])
    if file:
        result.save(file + '.png')
    
####################################

#adapterd from contours and bounding rectangle
def contourBands(filename):
    #https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contours_begin/py_contours_begin.html#contours-getting-started
    im = cv2.imread(filename)
    width,height=im.shape[0],im.shape[1]
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    contours,hierarchy=cv2.findContours(thresh,
    cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
    xoff,ratio,offset=Band.fitWindow(width,height)
    #https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html
    for i in range(len(contours)):
        x,y,w,h = cv2.boundingRect(contours[i])
        if 100>=w>=20 and h>=10:
            print ('cv2:',x,y,w,h)
            if xoff:
                Band(x*ratio+offset,y*ratio,w*ratio,h*ratio)
            else:
                Band(x*ratio,y*ratio+offset,w*ratio,h*ratio)    


#adapted from hough cilcle transformation
#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghcircles/py_houghcircles.html
def houghColonies(filename,data):
    img = cv2.imread(filename,0)
    width,height=img.shape[0],img.shape[1]
    img = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles=cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
            param1=40,param2=20,
            minRadius=data.colSize.minR,maxRadius=data.colSize.maxR)
    circles = np.uint16(np.around(circles))    
    
    xoff,ratio,offset=Col.fitWindow(width,height)
    
    for i in circles[0,:]:
        if xoff:
            Col(i[0]*ratio+offset,i[1]*ratio,i[2]*ratio)
        else:
            Col(i[0]*ratio,i[1]*ratio+offset,i[2]*ratio)
    
#this method wasn't very successful in recognizig plates, could've tried contour
# def houghPlates(filename,data):
#     img = cv2.imread(filename,0)
#     width,height=img.shape[0],img.shape[1]
#     img = cv2.medianBlur(img,5)
#     cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
#     #create a list of circles in the image
#     circles=cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
#             param1=40,param2=20,minRadius=200)
#     circles = np.uint16(np.around(circles))
#     
#     xoff,ratio,offset=Col.fitWindow(width,height)
#     
#     for i in circles[0,:]:
#             data.plates.append((i[0]*ratio+offset,i[1]*ratio,i[2]*ratio))

####################################

def listsProduct(lst1,lst2):
    assert(len(lst1)==len(lst2))
    result=[]
    for i in range(len(lst1)):
        result.append(lst1[i]*lst2[i])
    return result
    
def getLadderRegression(data):
    ladderSizes=[10000,8000,6000,5000,4000,3000,2500,2000,1500,1000,750,500,250]
    ladderLogs=list(map(lambda x: log(x), ladderSizes))
    ladderDist=[] #[84,7,509,87,48,97,81,93,248,34,76,74,374]
    for i in range(13):
        ladderDist.append(Band.ladder[i].y+Band.ladder[i].h/2)
    ladderDist.sort()
#reference: https://en.wikipedia.org/wiki/Simple_linear_regression
    xy=listsProduct(ladderDist,ladderLogs)
    xx=listsProduct(ladderDist,ladderDist)
    k=((mean(ladderDist)*mean(ladderLogs)-mean(xy)) /           (mean(ladderDist)*mean(ladderDist)-mean(xx)))
    b=mean(ladderLogs)-k*mean(ladderDist)

    return ladderSizes,ladderLogs,ladderDist,k,b

def drawRegressionLine(canvas,data):
    ladderSizes,ladderLogs,ladderDist,k,b=getLadderRegression(data)
    
    margin=50
    canvas.create_rectangle(3*margin,margin,data.width-3*margin,
    data.height-margin,fill='white')
    canvas.create_line(5*margin,2*margin,5*margin,
    data.height-3*margin)#ver
    canvas.create_line(5*margin,data.height-3*margin,data.width-4*margin,
    data.height-3*margin)#hor
    
    for i in range(13):
        relY=data.height-2*margin-(ladderLogs[i]-4.5)*100
        canvas.create_line(5*margin,relY,5*margin-3,relY)
        canvas.create_text(4*margin,relY,text='ln('+str(ladderSizes[i])+')')
        
        unitX=550/(ladderDist[12]-ladderDist[0])
        relX=300+(ladderDist[i]-ladderDist[0])*unitX
        canvas.create_oval(relX-2,relY-2,relX+2,relY+2)
        canvas.create_text(relX,data.height-2.5*margin,
        text=str(int(ladderDist[i])))
        
    startX=300
    startY=data.height-2*margin-(b+ladderDist[0]*k-4.5)*100
    endX=850
    endY=data.height-2*margin-(b+ladderDist[12]*k-4.5)*100

    canvas.create_line(startX,startY,endX,endY)
    
    canvas.create_text(data.width/2,data.height-2.1*margin,
    text='relative distance traveled')
    canvas.create_text(margin*4,margin*1.5,text='ln of\nmolecular\nsize(bp)')     
    canvas.create_text(data.width/2+margin,2*margin,
    text='ln(size)='+str(k)+'*distance+'+str(b))
