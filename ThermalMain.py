# -*- coding: utf-8 -*-
"""
Created on Mon May 25 14:16:24 2020

Thermal Curve Fit App
@author: Joshua Quintero
"""


from tkinter import *
from tkinter import filedialog
from tkinter import Text
from tkinter import simpledialog
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ThermalCurve import ThermalCurveFit
from tkinter.filedialog import asksaveasfile 
from tkinter.filedialog import askopenfilename 
import sys


class CustomDialog(simpledialog.Dialog):

    def __init__(self, parent, title=None, text=None):
        self.data = text
        simpledialog.Dialog.__init__(self, parent, title=title)

    def body(self, parent):

        self.text = Text(self, width=40, height=4)
        self.text.pack(fill="both", expand=True)

        self.text.insert("1.0", self.data)

        return self.text

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("Thermal Curve Fit")

     
        for r in range(16):
            self.master.rowconfigure(r, weight=1)    
      
        ascfile = open("asc.txt", "r")
        self.temp = ascfile.read()
        ascfile.close()
        self.asc_model = " "
        
        self.file = "t.PNG"
        self.c = ThermalCurveFit()
        Frame1 = Frame(master)
        Frame1.grid(row = 0, column = 0, rowspan = 1, columnspan = 1, sticky = W+E+N+S) 
        Frame2 = Frame(master)
        Frame2.grid(row = 5, column = 0, rowspan = 1, columnspan = 1, sticky = W+E+N+S)
        Frame3 = Frame(master)
        Frame3.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)
        self.Frame4 = Frame(master)
        self.Frame4.grid(row = 9, column = 2, rowspan = 3, columnspan = 3, sticky = W+E+N+S)
        Frame5 = Frame(master)
        Frame5.grid(row = 0, column = 1, rowspan = 1, columnspan = 1, sticky = W+E+N+S) 
        Frame6 = Frame(master)
        Frame6.grid(row = 5, column = 1, rowspan = 1, columnspan = 1, sticky = W+E+N+S)
        
        Frame7 = Frame(master)
        Frame7.grid(row = 6, column = 1, rowspan = 1, columnspan = 1, sticky = W+E+N+S)
        Frame8 = Frame(master)
        Frame8.grid(row = 6, column = 2, rowspan = 1, columnspan = 1, sticky = W+E+N+S)
        
        Frame9 = Frame(master)
        Frame9.grid(row = 6, column = 3, rowspan = 1, columnspan = 1, sticky = W+E+N+S)
        Frame10 = Frame(master)
        Frame10.grid(row = 6, column = 4, rowspan = 1, columnspan = 1, sticky = W+E+N+S)
        
        Frame11 = Frame(master)
        Frame11.grid(row = 8, column = 7, rowspan = 1, columnspan = 1, sticky = W+E+N+S)
        Frame12 = Frame(master)
        Frame12.grid(row = 8, column = 8, rowspan = 1, columnspan = 1, sticky = W+E+N+S)
        
        
        #setup image
        self.image = plt.imread("t.PNG")
        self.fig1 = plt.figure(figsize=(7,4))
        self.im = plt.imshow(self.image)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=Frame3)
        
        self.canvas1.get_tk_widget().pack()
        self.canvas1.draw()
        
        # set up min's and max
        labelymx = Label(Frame1, text = "ymax")
        labelymx.pack(fill = X)
        self.txt_ymx = Text(Frame5,width = 8, height = 1)
        self.txt_ymx.insert(END, "1000")
        self.txt_ymx.pack(fill = X)

        labelymn = Label(Frame2, text = "ymin")
        labelymn.pack(fill = X, side = BOTTOM)
        self.txt_ymn = Text(Frame6, width =8,height = 1)
        self.txt_ymn.insert(END, "0.1")
        self.txt_ymn.pack(fill = X, side = BOTTOM)
        
        labelxmin = Label(Frame7, text = "xmin")
        labelxmin.pack(fill = X, side = BOTTOM)
        self.txt_xmin = Text(Frame8, width =8,height = 1)
        self.txt_xmin.insert(END, "0.001")
        self.txt_xmin.pack(side = LEFT)
        
        
        self.txt_xmax = Text(Frame10, width =8,height = 1)
        self.txt_xmax.insert(END, "1000")
        self.txt_xmax.pack(side = RIGHT)  
        labelxmax = Label(Frame10, text = "xmax")
        labelxmax.pack(side = RIGHT)
    
        labelclip = Label(Frame11, text = "clip")
        labelclip.pack(fill = X, side = BOTTOM)
        self.txt_clip = Text(Frame12, width =8,height = 1)
        self.txt_clip.insert(END, "500")
        self.txt_clip.pack(side = LEFT)
        
        #setup plot
        self.fig = plt.figure(figsize=(7,4))
        self.a = self.fig.add_subplot(111)
        self.a.loglog([.1,1],[1,1],'bo', basex=10,basey=10)
        self.a.loglog([.1,1],[1,1],'ro', basex=10,basey=10)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.Frame4)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()
        
        #buttons
        self.Select_Btn = Button(master, text="Select Image", command = self.fileDialog).grid(row=7,column=3,sticky=E+W)
        self.Compute_Btn = Button(master, text="Compute", command = self.compute).grid(row=12,column=2,sticky=E+W)
        self.Save_Btn = Button(master, text="Save", command = self.save).grid(row=12,column=4,sticky=E+W)
       
        
        self.Exit_Btn = Button(master, text="Quit", command=self.close_app).grid(row=1, column= 8, sticky = E+W)
        

    def fileDialog(self):
        try:
            self.file = askopenfilename(initialdir = "/", title = "Select A png File", filetype = (("png", "*.png"),("All Files","*.*")))
        except AttributeError:
            pass
              # update image
        image = plt.imread(self.file)
        self.im.set_data(image)
        self.canvas1.draw()
        
    
    def close_app(self):
        self.destroy()
        sys.exit("quit")
        
    def save(self):
        
        if (self.asc_model !=" "):
            
            files = [('Spice', '*.asc'), ('All Files', '*.*')] 
            file = filedialog.asksaveasfile(initialdir = "/", filetypes = files, mode='w', defaultextension=".asc")
            if(file is None):
                return
            data = self.temp + self.asc_model
            file.write(data)
            file.close()
		
    def show_dialog(self):
        msg =".param r0 =  {} \n.param c0 =  {} \n.param r1 =  {} \n.param c1 =  {} \n.param r2 =  {} \n.param c2 =  {} \n.param r3 =  {} \n.param c3 =  {}".format(self.c.pre[0],self.c.pre[1],self.c.pre[2],self.c.pre[3],self.c.pre[4],self.c.pre[5],self.c.pre[6],self.c.pre[7])
        CustomDialog(self.master, title="Complete", text=msg)
    
    def compute(self):
        
        try:
            xmin = float(self.txt_xmin.get("1.0","end"))
            xmax = float(self.txt_xmax.get("1.0","end"))
            ymin = float(self.txt_ymn.get("1.0","end"))
            ymax = float(self.txt_ymx.get("1.0","end"))
            clip = float(self.txt_clip.get("1.0","end"))
            self.c.setFileName(self.file)
            self.c.setXAxis(xmin,xmax)
            self.c.setYAxis(ymin,ymax)
            self.c.setClip(clip)
            self.c.compute()
            self.a.cla()
            self.a.loglog(self.c.xtest,self.c.original,'ro', basex=10,basey=10)
            self.a.loglog(self.c.xtest,self.c.mod,'bo', basex=10,basey=10)

            print(self.file)
            #print (self.c.ymin,' ',self.c.ymax)
            print (self.c.mod)
            self.canvas.draw()
            
            self.update_idletasks()
            self.update()
            self.asc_model = "!.param r0 =  {} \\n.param c0 =  {} \\n.param r1 =  {} \\n.param c1 =  {} \\n.param r2 =  {} \\n.param c2 =  {} \\n.param r3 =  {} \\n.param c3 =  {}".format(self.c.pre[0],self.c.pre[1],self.c.pre[2],self.c.pre[3],self.c.pre[4],self.c.pre[5],self.c.pre[6],self.c.pre[7])
            #msg =".param r0 =  {} \n.param c0 =  {} \n.param r1 =  {} \n.param c1 =  {} \n.param r2 =  {} \n.param c2 =  {} \n.param r3 =  {} \n.param c3 =  {}".format(self.c.pre[0],self.c.pre[1],self.c.pre[2],self.c.pre[3],self.c.pre[4],self.c.pre[5],self.c.pre[6],self.c.pre[7])
            #messagebox.showinfo("Complete", msg)
            self.show_dialog()
        except ValueError:
            messagebox.showerror(title=None, message="Values are not numbers. Please fix")
         
  
 
    
if __name__ == "__main__":
      
    root = Tk()
    #root.geometry("400x200+200+200")
    app = Application(master=root)
    app.mainloop()