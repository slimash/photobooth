from tkinter import *
import PIL
from PIL import Image, ImageTk
from os import *
from picamera import PiCamera
from time import sleep
from datetime import *
from picamera import Color
from os import walk
import os
import datetime
import time
from glob import *
from os import listdir
import RPi.GPIO as GPIO

class MainGui:
  def __init__(self):
    self.cam = PiCamera()
    now = datetime.datetime.now()
    self.daytag = str(now.day) + "_" + str(now.month) + "_" + str(now.year) + "/"
    self.usbPfad = "/media/pi/BD23-DD96/FotoBox_Bilder/" #falls Stick vorhanden, dieser Pfad
    self.defPfad = "/home/pi/Bilder/" #falls kein Stick vorhanden, Verzeichnis auf microSD
    self.mainWindow = Tk()
    self.mainWindow.attributes("-fullscreen",True) #Vollbild Programm
    self.mainWindow.title("Fotobox")
    self.mainWindow.configure(background="#ffffff")
    self.mainWindow.geometry("1024x700")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setwarnings(False)
    
    #GPIO 21 - EINZELBILD
    #GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO 27 - SERIENBILD
    #GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO 17 - GALERIE
    #GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.add_event_detect(21,GPIO.RISING, callback=self.einzelbild_click, bouncetime=200)
    #GPIO.add_event_detect(27,GPIO.RISING, callback=self.serienbilder_click, bouncetime=200)
    #GPIO.add_event_detect(17,GPIO.RISING, callback=self.galerie_click, bouncetime=200)
  
#Header
    header = Frame(self.mainWindow,borderwidth=0)
    header.pack(side=TOP)
    img = ImageTk.PhotoImage(Image.open("/home/pi/Schreibtisch/FotoBox/0.png")) #Logo HSPF
    imgLabel = Label(header,text="HOCHSCHULE PFORZHEIM", font="Sans 20 bold" ,image = img,borderwidth=0)
    imgLabel.pack()
    
#Body
    frame = Frame(self.mainWindow,borderwidth=0)
    frame.configure(background="#ffffff")
    frame.pack(expand=NO,pady=20)
    
#Buttons Einzelbild, Serienbild, Galerie:
    Button(frame,borderwidth=2,text="Einzelbild",bg="#EBBB32",padx=8,pady=5, font="Sans 20 bold", height = 5, width = 15,command = self.einzelbild_click).pack(side=LEFT)
    Button(frame,borderwidth=2,text="Serienbild",bg="#EBBB32",padx=8,pady=5, font="Sans 20 bold", height = 5, width = 15,command=self.serienbilder_click).pack(side=LEFT)
    Button(frame,borderwidth=2,text="Galerie",bg="#EBBB32",padx=8,pady=5, font="Sans 20 bold", height = 5, width = 15,command = self.galerie_click).pack(side=LEFT)

#Footer
    footer = Frame(self.mainWindow,borderwidth=0)
    footer.configure(background="#ffffff")
    footer.pack(side=BOTTOM)
    self.lbl = Label(footer,bg="#ffffff",font="Sans 16 bold",fg="#F56363")
        self.lbl.pack()
    Button(footer,borderwidth=0,text="Programm Schließen",bg="#ffffff",font="Sans 14 bold",command=self.close_mainWindow).pack(side=TOP,padx=2,pady=60)
    self.mainWindow.mainloop()
    
#Einzelbild 1 Foto
    def einzelbild_click(self):
    self.take_photo(1)
    
    #Serienbild 4 Fotos
    def serienbilder_click(self):
    self.take_photo(4)

    def galerie_click(self):
    bilderList = []
    bilderList = glob(str(self.getFileDir()) + "*.jpg")
    if len(bilderList) == 0:
      self.lbl["text"] = "Galerie ist leer!"
      self.lbl.update()
      sleep(2)
      self.lbl["text"] = ""
      self.lbl.update()
    else:
      gallery = ImgWindow(bilderList,True)
      
    def close_mainWindow(self):
    self.mainWindow.destroy()
    
    def take_photo(self,bilderAnzahl):
    bilderList = []
    self.cam.start_preview()
    self.cam.resolution = (1020,480)
    for i in range(bilderAnzahl):
      self.cam.annotate_text_size = 50
      if bilderAnzahl > 1:
        self.cam.annotate_text = " Bild: " + str(i + 1) + " von " + str(bilderAnzahl) + " "
      else:
        self.cam.annotate_text = " Bereit ?! "
      sleep(2)
      pfadDir = str(self.getFileDir() + "Pic_" + str(int(time.time())) + ".jpg")
      self.cam.annotate_text = ""
      for i in range(8):
        self.cam.annotate_text_size = 100
        if 8 - i == 1:
          GPIO.output(19, GPIO.HIGH)
          self.cam.annotate_text = " Bitte laecheln :-) "
        else:
          self.cam.annotate_text = str(8 - i)
        sleep(1)
        
        self.cam.annotate_text = ""
        self.cam.capture(pfadDir)
        bilderList.append(pfadDir)
        GPIO.output(19, GPIO.LOW)
      self.cam.stop_preview()
      preview = ImgWindow(bilderList,False)
      
    def getFileDir(self):
      if os.path.isdir(self.usbPfad):
        if not os.path.isdir(str(self.usbPfad + self.daytag)):
          os.makedirs(self.usbPfad + self.daytag)
      return str(self.usbPfad + self.daytag)
      elif os.path.isdir(self.defPfad):
        if not os.path.isdir(self.defPfad + self.daytag):
          os.makedirs(self.defPfad + self.daytag)
      return str(self.defPfad + self.daytag)
        
class ImgWindow:
    def __init__(self,photoList,useGalleryGUI):
      self.pfad = []
      self.pfad = photoList
      self.useGalleryGUI = useGalleryGUI
      self.pointer = 0
      self.imgWindow = Toplevel()
      self.imgWindow.configure(background="#ffffff")
      self.imgWindow.attributes("-fullscreen",True)
      self.img = ImageTk.PhotoImage(Image.open(self.pfad[self.pointer]))
      self.panel = Label(self.imgWindow,bg="#ffffff",height=480,image = self.img)
      self.panel.pack(padx=2,pady=10,fill=BOTH,expand=YES)
      self.frame =Frame(self.imgWindow,bg="#ffffff")
      self.frame.pack(side=BOTTOM,fill=BOTH)
      if self.useGalleryGUI:
        Button(self.frame,text="<",bg="#EBBB32",fg="#ffffff",font="Sans 20 bold", height = 3, width = 10,command=self.showPrevPic).pack(side=LEFT)
        Button(self.frame,text=">",bg="#EBBB32",fg="#ffffff",font="Sans 20 bold", height = 3, width = 10,command=self.showNextPic).pack(side=RIGHT)
        Button(self.frame,borderwidth=0,text="Hauptmenü",bg="#ffffff",padx=1,pady=1, font="Sans 16 bold",command=self.closeWindow).pack(side=BOTTOM,ipady=20)
      else:
        Button(self.frame,text="Behalten",bg="#1ca706",fg="#ffffff",font="Sans 20 bold", height = 3, width = 10,command=self.keepImg).pack(side=LEFT)
        Button(self.frame,text="Löschen",bg="#993232",fg="#ffffff",font="Sans 20 bold", height = 3, width = 10,command=self.delete_image).pack(side=RIGHT)
      txtLabel = str(1) + " von " + str(len(self.pfad))
      self.l = Label(self.frame,bg="#ffffff",font="Sans 16 bold",fg="#EBBB32",text=txtLabel)
      self.l.pack(side=TOP)
      self.makePreview(0)
      self.imgWindow.mainloop()
      
    def closeWindow(self):
      self.imgWindow.destroy()
      
    def makePreview(self,pointer):
      self.img = ImageTk.PhotoImage(Image.open(self.pfad[pointer]))
      self.panel["image"] = self.img
      self.l["text"] = str(pointer + 1) + " von " + str(len(self.pfad))
      self.l.update()
      
    def showNextPic(self):
      if self.pointer + 1 < len(self.pfad):
        self.pointer +=1
      else:
        self.pointer = 0
      self.makePreview(self.pointer)
      
    def showPrevPic(self):
      if self.pointer > 0:
        self.pointer -= 1
      else:
        self.pointer = len(self.pfad) - 1
      self.makePreview(self.pointer)
      
    def keepImg(self):
      if self.pointer < len(self.pfad) - 1:
        self.pointer += 1
        self.makePreview(self.pointer)
      else:
        self.closeWindow()
        
    def delete_image(self):
      if path.exists(str(self.pfad[self.pointer])):
        remove(str(self.pfad[self.pointer]))
      if self.pointer < len(self.pfad) - 1:
        self.pointer += 1
        self.makePreview(self.pointer)
      else:
        self.closeWindow()
        
#"App" erstellen
photobox = MainGui()
GPIO.cleanup()
