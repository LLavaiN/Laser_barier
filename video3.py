import cv2 as cv
import tkinter
import numpy
import serial
import time
from tkinter import *
from tkinter import ttk

def forbut(event):
    global numb

    numb = int(ent.get())
    ser.write(b'1')
    time.sleep(0.1)
    iii.destroy()

def forio(event):
    ser.write(b'2')
    time.sleep(0.1)
def forbbb(event):
   
    global ideal 
    ideal = cv.countNonZero(roImgBin)

ser = serial.Serial('COM3', 9600)    
iii = Tk()
iii.title("Выбор камеры")
lab = ttk.Label(iii, text="Введите номер камеры", style="BW.TLabel")
ent = ttk.Entry(iii, width = 3)
but = ttk.Button(iii, text = "OK")
but.bind("<Button-1>",forbut)
lab.pack()
ent.pack()
but.pack()
iii.mainloop()



ideal = 1
fff = 1


root = Tk()
st = BooleanVar()
st.set(0)
root.title("Настройки")
lamp = Toplevel(root)
lamp.title("Маркер")
labb = Label(lamp, width = 30, height = 15, text = "Установите значение")
cap = cv.VideoCapture(numb)
labLow = ttk.Label(root, text="Границы низкого уровня", style="BW.TLabel")
labHigh = ttk.Label(root, text="Границы высокого уровня", style="BW.TLabel")
LowR = Scale(root, orient=HORIZONTAL,length=511,from_=0,to=255)
LowG = Scale(root, orient=HORIZONTAL,length=511,from_=0,to=255)
LowB = Scale(root, orient=HORIZONTAL,length=511,from_=0,to=255)
HighR = Scale(root, orient=HORIZONTAL,length=511,from_=0,to=255)
HighG = Scale(root, orient=HORIZONTAL,length=511,from_=0,to=255)
HighB = Scale(root, orient=HORIZONTAL,length=511,from_=0,to=255)

bbb = ttk.Button(root, text="Установить опорное значение")
bbb.bind("<Button-1>", forbbb)

io = ttk.Button(root, text="Включить/Выключить лазер")
io.bind("<Button-1>", forio)

labD = ttk.Label(root, text = 'Показатель с датчиков', style="BW.TLabel")

rb1 = Radiobutton(root, text="Авто", value = 1, variable = st)
rb2 = Radiobutton(root, text="Ручная", value = 0, variable = st)
labLow.pack()
LowR.pack()
LowG.pack()
LowB.pack()
labHigh.pack()
HighR.pack()
HighG.pack()
HighB.pack()
bbb.pack()
io.pack()
rb1.pack()
rb2.pack()
labb.pack()
labD.pack()
i = 0

while (True):
    
    root.update()
    lamp.update()

    labD.config(text = ser.readline())
   
    #time.sleep(0.1)
    ret,frame = cap.read()
    frameCopy = frame.copy()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    hsv = cv.blur(hsv,(5,5))
    mask = cv.inRange(hsv,(LowB.get(),LowG.get(),LowR.get()),(HighB.get(),HighG.get(),HighR.get()))
    if(st.get() == True):
        LowB.set(0)
        LowG.set(0)
        LowR.set(249)
        HighB.set(102)
        HighG.set(139)
        HighR.set(255)
    #cv.imshow("mask", mask)
    #mask = cv.inRange(hsv,(100,100,100),(255,255,255))
    #cv.imshow("Binary", mask)
    maskEr = cv.erode(mask,(6,6),iterations=2)
    #cv.imshow("maskEr",maskEr)
    maskDi = cv.dilate(mask,(6,6), iterations=4)
    #cv.imshow("maskDi",maskDi)
    result = cv.bitwise_and(frame, frame, mask=mask)
    #cv.imshow("Frame", frame)

    contours = cv.findContours(mask, cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
    contours=contours[1]
    contours=sorted(contours,key=cv.contourArea,reverse=True)
   
    
   
  
    if contours:
        cv.drawContours(result,contours[0],-1,(255,0,255),3)
        (x,y,w,h) = cv.boundingRect(contours[0])
        rect = cv.rectangle(mask,(x,y),(x+w,y+h),(0,255,0),2)
 
        roImg=frameCopy[y:y+h,x:x+w]
        roImgBin=mask[y:y+h,x:x+w]
        cv.imshow("Detect", roImg)
        
        fff = cv.countNonZero(roImgBin)
        if ideal != 1 and ideal != 0:
            
            proc = int(fff*100/ideal)
            new = str(proc)+"%"
            labb.config(text = new)
           
            if proc <=70:
                labb.config(bg = "red")
                
                
            else:
                labb.config(bg = "green")
               
            
    else:
        labb.config(text = "0%", bg = "red")
         
        
    cv.imshow("Result", result)
    if cv.waitKey(1) == ord("q"):
        break
cap.release()
ser.write(b'0')
time.sleep(0.1)
root.destroy()
cv.destroyAllWindows()

