from tkinter import *
from PIL import Image, ImageTk, ImageGrab
from helpers import *
from objects import *

'''
This file contains the run function that pulls everything together and the UI
adapted from the mode-demo animation framework on the 112 course website. (https://www.cs.cmu.edu/~112/notes/notes-animations-demos.html)
More complex mouse events are added for the purpose of this app.
'''
    
def homeMousePressed(event, data):
    x=event.x
    y=event.y
    if 0<=x<=500 and 150<=y<=650:
        loadImage(data)
        if data.img!='':
            data.mode='gelMode'
        Band.bands.clear()
    elif 600<=x<=1100 and 150<=y<=650:
        loadImage(data)
        if data.img!='':
            data.mode='plateMode'
        Col.colonies.clear()

def homeMousePosition(event,data):
    x=event.x
    y=event.y
    if 0<=x<=500 and 150<=y<=650:
        data.gelInstruction=True
    elif 600<=x<=1100 and 150<=y<=650:
        data.pltInstruction=True
    else:
        data.gelInstruction=False
        data.pltInstruction=False

def homeRedrawAll(canvas, data):
    canvas.create_text(data.width//2,30,
    anchor='n',text='FADs Lab Assistant',fill='white',
    font="Courier " + str(35) + " bold")
    
    canvas.gelIcon=data.gelIcon
    canvas.create_image(250,400,image=canvas.gelIcon)
    
    canvas.plateIcon=data.plateIcon
    canvas.create_image(850,400,image=canvas.plateIcon)
    
    canvas.create_text(data.width//2-300,110,anchor='n',
    text='click below to interpret argorose gel',fill='white',
    font="Courier " + str(15))
    canvas.create_text(data.width//2+300,110,anchor='n',
    text='click below to count yeast colonies',fill='white',
    font="Courier " + str(15))
    
    if data.gelInstruction:
        fakeTransparentRect(canvas,0,150,500,650)
        canvas.create_text(3,153,anchor='nw',
    text='Basing on the bands in the ladder lane,\ngenerate a formula that converts molecule\nmigration distance in gel to molecule\nsize. Measure the distance between the\nsample bands and the wells, and\ncalculate the molecule size with the\nformula and the measurement.\n'+'\nNote(from wikipedia):\nThe 1kb DNA ladder we use is a set\nof standards that are used to identify\nthe approximate size of a molecule\nrun on a gel during electrophoresis,\nusing the principle that molecular\nweight is inversely proportional to\nmigration rate through a gel matrix.\nTherefore, when used in gel\nelectrophoresis, markers effectively\nprovide a logarithmic scale by\nwhich to estimate the size\nof the other fragments.',
    font="Courier " + str(20))
    elif data.pltInstruction:
        fakeTransparentRect(canvas,600,150,1100,650)
        canvas.create_text(603,153,anchor='nw',
    text='The program will detect circles basing\non default settings. Users can\nadjust the settings for better result,\nor manually delete or draw circle marks.\nThen, the number of circles/colonies\nwill be counted and displayed.\nUsers can also set a radius as\nthe standard for robust growth.\n\nNote:\nAfter plating transformed yeasts\non dozens of different selection plates,\nwe need to count\'em up!\nLet alone being lazy, there is\na situation called TMTC, too many\nto count due to human counting ability.\nHopefully computers don\'t have such prblems.',
    font="Courier " + str(20))

####################################

def gelRedrawAll(canvas,data):
    canvas.bgImage=data.actualImage
    canvas.create_image(data.width//2,data.height//2,
    image=canvas.bgImage)
    
    for band in Band.bands:
        band.draw(canvas)
    
    if data.curMove!=[]: 
        canvas.create_rectangle(data.curMove[0][0],data.curMove[0][1],
        data.curMove[-1][0],data.curMove[-1][1],outline='white')
    
    if data.ladder!=[]:    
        canvas.create_rectangle(data.ladder[0],data.ladder[1],data.ladder[2],
        data.ladder[3],outline='green',width=3)
    
    data.home.draw(canvas)
    data.recognize.draw(canvas)
    data.customize.draw(canvas)
    data.analyze.draw(canvas)
    
    if data.customizing:
        canvas.create_text(data.width//2,20,anchor='n',
        text='please carefully mark out the 1kb ladder lane\n(make sure to include all 13 ladder bands!)',
        fill='white',font="Courier " + str(18))
        data.done.draw(canvas)
    else:
        canvas.create_text(data.width//2,data.height-15,anchor='n',
        text='you may mark out bands on the gel by hand andclick on the mark to remove it',
        fill='white',font="Courier " + str(13))
    

def gelMousePressed(event,data):
    if data.home.clicked(event.x,event.y):
        data.mode='home'
    elif data.recognize.clicked(event.x,event.y):
        contourBands(data.img)
    elif data.customize.clicked(event.x,event.y):
        data.customizing=not data.customizing
    elif data.analyze.clicked(event.x,event.y):
        for band in Band.bands:
            if data.ladder!=[] and band.inLadder(data): #short-circuit
                Band.ladder.append(band)
        print (len(Band.ladder))
        if len(Band.ladder)==13:
            data.mode='gelResult'
        else:
            data.ladder=[]
            Band.ladder=[]
            data.customizing=True
    for band in Band.bands:
        band.remove(event.x,event.y)

def gelMousePosition(event,data):
    if data.home.clicked(event.x,event.y): 
        data.home.over=True
    elif data.recognize.clicked(event.x,event.y):
        data.recognize.over=True
    elif data.customize.clicked(event.x,event.y):
        data.customize.over=True
    elif data.analyze.clicked(event.x,event.y):
        data.analyze.over=True
    else:
        data.home.over=False
        data.recognize.over=False
        data.customize.over=False
        data.analyze.over=False
        
def gelMouseMoved(event,data):
    data.curMove.append((event.x,event.y))
    
def gelMouseReleased(event,data,canvas):
    if data.customizing:
        if data.curMove!=[]:
            data.ladder.append(data.curMove[0][0])
            data.ladder.append(data.curMove[0][1])
            data.ladder.append(event.x)
            data.ladder.append(event.y)
            data.curMove=[]
    else:
        if data.curMove!=[]:
            w=abs(data.curMove[0][0]-event.x)
            h=abs(data.curMove[0][1]-event.y)
            Band(data.curMove[0][0],data.curMove[0][1],w,h)
            data.curMove=[]

####################################

def pltRedrawAll(canvas,data):
    canvas.bgImage=data.actualImage
    canvas.create_image(data.width//2,data.height//2,
    image=canvas.bgImage)
    
    for col in Col.colonies:
        col.draw(canvas)
    
    if data.curMove!=[]: 
        canvas.create_oval(data.curMove[0][0],data.curMove[0][1],
        data.curMove[-1][0],data.curMove[-1][1],outline='white')
    
    if data.plates!=[]:
        for i in data.plates:    
            canvas.create_oval(i[0],i[1],i[2],i[3],outline='green',width=3)
            canvas.create_text((i[0]+i[2])/2,i[1],
        text='plate '+str(data.plates.index(i)+1) ,
        fill='green',font="Courier 18 bold")
    
    data.home.draw(canvas)
    data.recognize.draw(canvas)
    data.customize.draw(canvas)
    data.analyze.draw(canvas)
            
    if data.customizing:
        data.colSize.draw(canvas)
        data.done.draw(canvas)
        canvas.create_text(data.width//2,data.height-10,anchor='s',
        text='please circle out each individual plate before analyzing',
        fill='white',font="Courier 18")
    else:
        canvas.create_text(data.width//2,data.height-15,anchor='n',
        text='you may mark out colonies by hand and click on the mark to remove it',
        fill='white',font="Courier " + str(13))


def pltMousePressed(event,data):
    if data.home.clicked(event.x,event.y):
        data.mode='home'
    elif data.recognize.clicked(event.x,event.y):
        houghColonies(data.img,data)
        #houghPlates(data.img,data)
    elif data.customize.clicked(event.x,event.y):
        if data.customizing:
            Col.colonies.clear()
            houghColonies(data.img,data)
        data.customizing=not data.customizing
    elif data.analyze.clicked(event.x,event.y):
        if data.plates!=[]:
            data.mode='pltResult'
        else:
            data.customizing=True
    if data.customizing:
        data.colSize.selectV(event.x,event.y)
    for col in Col.colonies:
        col.remove(event.x,event.y)
        
def pltMouseMoved(event,data):
    if data.colSize.select!=None:
        data.colSize.drag(event.x,event.y)
    else:
        data.curMove.append((event.x,event.y))
        
def pltMousePosition(event,data):
    if data.home.clicked(event.x,event.y): 
        data.home.over=True
    elif data.recognize.clicked(event.x,event.y):
        data.recognize.over=True
    elif data.customize.clicked(event.x,event.y):
        data.customize.over=True
    elif data.analyze.clicked(event.x,event.y):
        data.analyze.over=True
    else:
        data.home.over=False
        data.recognize.over=False
        data.customize.over=False
        data.analyze.over=False
    
def pltMouseReleased(event,data,canvas):
    if data.customizing:
        if data.colSize.select!=None:
            print('r')
            data.colSize.set(event.x,event.y)
        else:
            if data.curMove!=[]:
                data.plates.append((data.curMove[0][0],data.curMove[0][1],event.x,
                event.y))
                Col.plates[len(data.plates)]=set()
                data.curMove=[]
    else:
        if data.curMove!=[]:
            x=(data.curMove[0][0]+event.x)/2
            y=(data.curMove[0][1]+event.y)/2
            r=(abs(data.curMove[0][0]-event.x)+abs(data.curMove[0][1]-event.y))/4
            Col(x,y,r)
            data.curMove=[]

####################################

def gelRRedrawAll(canvas,data):
    if data.fin:
        canvas.bgImage=data.actualImage
        canvas.create_image(data.width//2,data.height//2,image=canvas.bgImage)
        ladderSizes,ladderLogs,ladderDist,k,b=getLadderRegression(data)
        for band in Band.bands:
            if not band in Band.ladder:
                band.draw(canvas)
                size=int(e**((band.y+band.h/2)*k+b))
                canvas.create_text(band.x+band.w,band.y,text=str(size)+'\n   bp',
                fill='green yellow', font="Courier")
    else:
        data.next.draw(canvas)
        drawRegressionLine(canvas,data)
        
    data.home.draw(canvas)
    data.back.draw(canvas)
    data.save.draw(canvas)
    
def gelRMousePressed(event, data):
    if data.home.clicked(event.x,event.y):
        data.mode='home'
    elif data.back.clicked(event.x,event.y):
        data.mode='gelMode'
    elif data.save.clicked(event.x,event.y):
        save(data)
    elif data.next.clicked(event.x,event.y):
        data.fin=True
        
def gelRMousePosition(event,data):
    if data.save.clicked(event.x,event.y):
        data.save.over=True
    elif data.home.clicked(event.x,event.y):
        data.home.over=True
    else:
        data.save.over=False
        data.home.over=False

####################################        

def pltRRedrawAll(canvas, data):
    canvas.bgImage=data.actualImage
    canvas.create_image(data.width//2,data.height//2,image=canvas.bgImage)

    for col in Col.colonies:
        col.inPlate(data)
        col.draw(canvas)
    
    for i in data.plates:    
        canvas.create_oval(i[0],i[1],i[2],i[3],outline='green',width=3)
        canvas.create_text((i[0]+i[2])/2,i[1],
        text='plate '+str(data.plates.index(i)+1),
        fill='green',font="Courier 18 bold")
        numCols=len(Col.plates[data.plates.index(i)+1])
        canvas.create_text((i[0]+i[2])/2,i[3],text=str(numCols)+' colonies',
        fill='green yellow',font="Courier 18 bold")
        
    data.home.draw(canvas)
    data.back.draw(canvas)
    data.save.draw(canvas)
    
def pltRMousePressed(event, data):
    if data.home.clicked(event.x,event.y):
        data.mode='home'
    elif data.back.clicked(event.x,event.y):
        data.mode='plateMode'
    elif data.save.clicked(event.x,event.y):
        save(data)
        
def pltRMousePosition(event,data):
    if data.save.clicked(event.x,event.y):
        data.save.over=True
    elif data.home.clicked(event.x,event.y):
        data.home.over=True
    else:
        data.save.over=False
        data.home.over=False
        
####################################

def init(data):
    #general
    data.mode='home'
    data.img=None
    data.actualImage=None
    data.curMove=[]
    data.customizing=False
    data.fin=False
    data.ladder=[]
    data.plates=[]
    data.gelInstruction=False
    data.pltInstruction=False
    #icons
    img0=Image.open('gelIcon.png')
    img0=img0.resize((500,500),Image.ANTIALIAS)
    gelIcon=ImageTk.PhotoImage(img0)
    data.gelIcon=gelIcon
    img1=Image.open('plateIcon.png')
    img1=img1.resize((500,500),Image.ANTIALIAS)
    plateIcon=ImageTk.PhotoImage(img1)
    data.plateIcon=plateIcon
    #objects
    data.home=Button(70,data.height-15,'HOME',expl='to the home page')
    data.recognize=Button(70,15,'RECOGNIZE',expl='click to draw marks on\nopencv recognized features')
    data.back=Button(70,15,'BACK')
    data.customize=Button(data.width-70,15,'CUSTOMIZE',expl='click to provide info\non the ladder/plates')
    data.done=Button(data.width-70,15,'DONE')
    data.save=Button(data.width-70,15,'SAVE',expl='save result as png image')
    data.analyze=Button(data.width-70,data.height-15,'ANALYZE',expl='click to generate result')
    data.next=Button(data.width-70,data.height-15,'NEXT')
    data.colSize=DragBar(1,20)

def mousePressed(event, data):
    if data.mode=='home': homeMousePressed(event, data)
    elif data.mode=='gelMode': gelMousePressed(event, data)
    elif data.mode=='plateMode': pltMousePressed(event, data)
    elif data.mode=='gelResult': gelRMousePressed(event, data)
    elif data.mode=='pltResult': pltRMousePressed(event, data)

def mouseMoved(event,data):
    if data.mode=='home': homeMouseMoved(event, data)
    elif data.mode=='gelMode': gelMouseMoved(event,data)
    elif data.mode=='plateMode': pltMouseMoved(event,data)
    
def mouseReleased(event,data,canvas):
    if data.mode=='gelMode': gelMouseReleased(event,data,canvas)
    elif data.mode=='plateMode': pltMouseReleased(event,data,canvas)
    
def mousePosition(event,data):
    if data.mode=='home': homeMousePosition(event, data)
    #incomplete feature
    elif data.mode=='gelMode': gelMousePosition(event,data)
    elif data.mode=='plateMode': pltMousePosition(event,data)
    elif data.mode=='gelResult': gelRMousePosition(event,data)
    elif data.mode=='pltResult': pltRMousePosition(event,data)

def redrawAll(canvas, data):
    if data.mode=='home': homeRedrawAll(canvas, data)
    elif data.mode=='gelMode': gelRedrawAll(canvas, data)
    elif data.mode=='plateMode': pltRedrawAll(canvas, data)
    elif data.mode=='gelResult': gelRRedrawAll(canvas, data)
    elif data.mode=='pltResult': pltRRedrawAll(canvas, data)

####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
        fill='gray13', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def mouseMovedWrapper(event, canvas, data):
        mouseMoved(event, data)
        redrawAllWrapper(canvas, data)
        
    def mouseReleasedWrapper(event, canvas, data):
        mouseReleased(event,data,canvas)
        redrawAllWrapper(canvas, data)
        
    def mousePositionWrapper(event, canvas, data):
        mousePosition(event,data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False)

    #root.event_generate("<Motion>",x=0,y=0)

    init(data)
    
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    
    # set up events
    root.bind("<Button-1>", lambda event:
                        mousePressedWrapper(event, canvas, data))
    root.bind("<B1-Motion>", lambda event:
                        mouseMovedWrapper(event, canvas, data))
    root.bind("<ButtonRelease-1>", lambda event:
                        mouseReleasedWrapper(event, canvas, data))
    root.bind("<Motion>", lambda event:
                        mousePositionWrapper(event, canvas, data))
    
    root.mainloop() 

run(1100, 700)