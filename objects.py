#from helpers import fakeTransparentRect
def fakeTransparentRect(canvas,x1, y1, x2, y2):
    for i in range(x1,x2,2):
        canvas.create_line(i,y1,i,y2,fill='gray81')
    for i in range(y1,y2,3):
        canvas.create_line(x1,i,x2,i,fill='white')
    canvas.create_rectangle(x1, y1, x2, y2,width=3,outline='white')
    
'''
This file contains all the objects constructed for the app.
There are two major categories: Marks and widget imitations. Marks objects
integrate the opencv recognized shapes with the user-drawn ones. The tkinter
widget imitations are more compatible with canvas and nicer-looking.
'''

class Mark(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def fitWindow(h,w):
        ratio0=w/h
        parameter=[]
        if ratio0>(1100/700):
            ratio=1100/w
            offset=(700-ratio*h)/2
            parameter.append(False)
        else:
            ratio=700/h
            offset=(1100-ratio*w)/2
            parameter.append(True)
        parameter.append(ratio)
        parameter.append(offset)
        return parameter
        
class Band(Mark):
    bands=[]
    ladder=[]
    
    def __init__(self,x,y,w,h,bands=bands):
        super().__init__(x,y)
        self.w=w
        self.h=h
        bands.append(self)
        print('tk:',self)
    
    def draw(self,canvas):
        canvas.create_rectangle(self.x,self.y,self.x+self.w,self.y+self.h,
            outline='green yellow')
            
    def remove(self,x,y,bands=bands):
        if self.x <x< self.x+self.w and self.y <y< self.y+self.h:
            print('pop',self)
            bands.remove(self)
    
    def inLadder(self,data):
        x1,y1,x2,y2=data.ladder[0],data.ladder[1],data.ladder[2],data.ladder[3]
        if x1<self.x<x2 and x1<self.x+self.w<x2 \
            and y1<self.y<y2 and y1<self.y+self.h<y2:
                return True
        else: return False
        
    def __repr__(self):
        return str(int(self.x))+' '+str(int(self.y))+' '+str(int(self.w))+' '+str(int(self.h))
        
class Col(Mark):
    colonies=[]
    plates=dict()
    
    def __init__(self,x,y,r,colonies=colonies):
        super().__init__(x,y)
        self.r=r
        colonies.append(self)
        print(self)
    
    def draw(self,canvas):
        canvas.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,
        self.y+self.r,outline='green yellow')
            
    def remove(self,x,y,colonies=colonies):
        d=((self.x-x)**2+(self.y-y)**2)**0.5
        if d<=self.r:
            colonies.remove(self)
    
    def __repr__(self):
        return str(int(self.x))+' '+str(int(self.y))+' '+str(int(self.r))
    
    def inPlate(self,data):
        for i in data.plates:
            x1,y1,x2,y2=i[0],i[1],i[2],i[3]
            if x1<self.x<x2 and y1<self.y<y2:
                Col.plates[data.plates.index(i)+1].add(self)

####################################
    
class Button(object):
    def __init__(self,x,y,text,expl=None,over=False):
        self.x=x
        self.y=y
        self.text=text
        self.over=over
        self.expl=expl
    
    def draw(self,canvas):
        for i in range(7):
            canvas.create_rectangle(self.x+70-i*5,self.y+15-i*1,self.x-70+i*5,
            self.y-15+i*1,fill='gray'+str(80-i*10),width=0)
        canvas.create_text(self.x,self.y,text=self.text,
        fill='white',font="Courier " + str(21))
        #incomplete feature
        if self.over:
            fakeTransparentRect(canvas,300,300,800,400)
            canvas.create_text(550,350,text=self.expl,font="Courier " + str(18),
            fill='black')
    
    def clicked(self,x,y):
        if self.x-70 <x< self.x+70 and self.y-15 <y< self.y+15:
            return True
        else: return False
        
class DragBar(object):
    def __init__(self,minR,maxR,select=None):
        self.minR=minR
        self.maxR=maxR
        self.select=select
    
    def draw(self,canvas):
        minR=self.minR*3+400
        maxR=self.maxR*3+400
        fakeTransparentRect(canvas,300,0,800,70)
        canvas.create_line(400,30,700,30,width=3,fill='white')
        canvas.create_line(minR,20,maxR,20,width=3,fill='green yellow')
        canvas.create_oval(minR-5,15,minR+5,32,fill='white')
        canvas.create_oval(maxR-5,15,maxR+5,32,fill='white')
        canvas.create_text(minR,50,text=str(self.minR),fill='green yellow',
        font="Courier 20 bold")
        canvas.create_text(maxR,50,text=str(self.maxR),fill='green yellow',
        font="Courier 20 bold")
        canvas.create_text(350,35,text='Min\nColony\nSize',fill='black',
        font="Courier 15 bold")
        canvas.create_text(750,35,text='Max\nColony\nSize',fill='black',
        font="Courier 15 bold")
        
    def selectV(self,x,y):
        minR=self.minR*3+400
        maxR=self.maxR*3+400
        if 13<y<35:
            if minR-5<x<minR+5:
                self.select='minR'
            elif maxR-5<x<maxR+5:
                self.select='maxR'
        else: self.select=None
    
    def drag(self,x,y):
        if self.select=='minR':
            self.minR=int((x-400)/3)
        elif self.select=='maxR':
            self.maxR=int((x-400)/3)
    
    def set(self,x,y):
        if self.select=='minR':
            self.minR=int((x-400)/3)
            self.select=None
        elif self.select=='maxR':
            self.maxR=int((x-400)/3)
            self.select=None