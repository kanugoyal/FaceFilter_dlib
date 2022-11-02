from tkinter import *
import cv2
import threading
import datetime
import os
import time
from PIL import Image, ImageTk
from FaceFilters import FaceFilters

class GUIFace:
	def __init__(self, vs, fc, outPath):
		self.vs = vs
		self.fc = fc
		self.outPath = outPath
		self.frame = None
		self.thread = None
		self.stopEvent = None
		self.filterChoice = None
		# initialize the root window and video panel
		self.root = Tk()
		self.panel = None


		self.center = Frame(self.root, width=150, height=40,padx=10, pady=10)
		btm_frame = Frame(self.root, bg='white', width=450, height=45, padx=3, pady=3)
		btm_frame2 = Frame(self.root, bg='white', width=450, height=60)

		# layout all of the main containers
		self.root.grid_rowconfigure(1, weight=1)
		self.root.grid_columnconfigure(0, weight=1)

		self.center.grid(row=1)
		btm_frame.grid(row=3)
		btm_frame2.grid(row=4)


		# create the center widgets
		self.center.grid_rowconfigure(1, weight=1)
		self.center.grid_columnconfigure(1, weight=1)

		#panel = Frame(center, bg='yellow', width=250, height=210, padx=3, pady=3)
		#ctr_mid.grid(row=0, column=1, sticky="nsew")

		# create the bottom widgets
		btn1 = Button(btm_frame, text='Glasses', command=lambda: self.setFilterChoice(0), width = 15, fg = "black", bg = "gray", bd = 0)
		btn2 = Button(btm_frame, text='Eyes', command=lambda: self.setFilterChoice(1), width = 15, fg = "black", bg = "gray", bd = 0)
		btn3 = Button(btm_frame, text='Eyeglasses', command=lambda: self.setFilterChoice(2), width = 15, fg = "black", bg = "gray", bd = 0)
		btn4 = Button(btm_frame, text='3DGlasses', command=lambda: self.setFilterChoice(3), width = 15, fg = "black", bg = "gray", bd = 0)
		btn5 = Button(btm_frame, text='Swag Glasses', command=lambda: self.setFilterChoice(4), width = 20, fg = "black", bg = "gray", bd = 0)
		btn6 = Button(btm_frame, text='Cat', command=lambda: self.setFilterChoice(5), width = 20, fg = "black", bg = "gray", bd = 0)
		btn7 = Button(btm_frame, text='Monkey', command=lambda: self.setFilterChoice(6), width = 15, fg = "black", bg = "gray", bd = 0)
		btn8 = Button(btm_frame, text='Rabbit', command=lambda: self.setFilterChoice(7),  width = 15,fg = "black", bg = "gray", bd = 0)
		btn9 = Button(btm_frame, text='Moustache1', command=lambda: self.setFilterChoice(8), width = 15, fg = "black", bg = "gray", bd = 0)
		btn10 = Button(btm_frame, text='Moustache2', command=lambda: self.setFilterChoice(9), width = 15, fg = "black", bg = "gray", bd = 0)
		btn11 = Button(btm_frame, text='Ironman', command=lambda: self.setFilterChoice(10), width = 15, fg = "black", bg = "gray", bd = 0)
		btn12 = Button(btm_frame, text='Spiderman', command=lambda: self.setFilterChoice(11), width = 20, fg = "black", bg = "gray", bd = 0)
		btn13 = Button(btm_frame, text='Batman', command=lambda: self.setFilterChoice(12), width = 20, fg = "black", bg = "gray", bd = 0)
		btn14 = Button(btm_frame, text='Captain America', command=lambda: self.setFilterChoice(13), width = 15, fg = "black", bg = "gray", bd = 0)

		# layout the widgets in bottom frame
		btn1.grid(row=0, column=1)
		btn2.grid(row=0, column=2)
		btn3.grid(row=0, column=3)
		btn4.grid(row=0, column=4)
		btn5.grid(row=0, column=5)
		btn6.grid(row=0, column=6)
		btn7.grid(row=0, column=7)
		btn8.grid(row=1, column=1)
		btn9.grid(row=1, column=2)
		btn10.grid(row=1, column=3)
		btn11.grid(row=1, column=4)
		btn12.grid(row=1, column=5)
		btn13.grid(row=1, column=6)
		btn14.grid(row=1, column=7)

		# create the bottom2 widgets
		btm_frame2.grid_columnconfigure(1, weight=1)
		snapbtn = Button(btm_frame2, text='Snap', command=self.takeSnapshot, width = 80, height=2, fg = "black", bg = "lime green", bd = 1)
		snapbtn.grid(row=0, column=0,columnspan=3)

		# start a thread that constantly pools video sensor for most recently read frame
		self.stopEvent = threading.Event()
		self.videoLoop()

		#self.root.geometry('800x610')
		self.root.wm_title('Face Filters')
		self.root.wm_protocol('WM_DELETE_WINDOW', self.onClose)
		self.root.mainloop()
	
	def videoLoop(self):
		try:

			if not self.stopEvent.is_set():
				# keep looping over frames until instructed to stop
				self.frame = self.vs.read()
				if self.filterChoice!=None:
					self.frame = self.fc.applyFilter(self.frame, self.filterChoice)
				self.frame = cv2.flip(self.frame, 1)
				cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
				img = Image.fromarray(cv2image)
				img = ImageTk.PhotoImage(image=img)

				# if panel in not None, we need to initialize it
				if self.panel is None:
					self.panel = Label(self.center,image=img)
					self.panel.image = img
					#self.panel.pack(side='left', expand='yes', padx=10, pady=10)
					self.panel.grid(row=0, column=1, sticky="nsew")

				else:
					self.panel.configure(image=img)
					self.panel.image = img
				self.panel.after(10,self.videoLoop)
		except Exception as e:
			print("[ERROR] {}".format(e))

	def setFilterChoice(self, n):
		self.filterChoice = n
		print('[INFO] Filter selected: {}'.format(self.fc.filters[n]))

	def takeSnapshot(self):
		# grab current timestamp and construct the output path
		ts = datetime.datetime.now()
		filename = '{}.jpg'.format(ts.strftime('%Y%b%d_%H%M%S'))
		p = os.path.sep.join((self.outPath, filename))

		# save file
		cv2.imwrite(p, self.frame.copy())
		print("[INFO] saved {}".format(filename))

	def onClose(self):
		# set stop event, cleanup the camera
		# allow rest of the quit process to continue
		print("[INFO] closing...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()