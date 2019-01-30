from tkinter import *
from tkinter import filedialog
class GUI:

    def __init__(self):
        self.root = Tk()
        self.root.minsize(width=500,height=400)
        self.frame = Frame(self.root)
        self.frame.pack_propagate(0)
        self.frame.pack(fill=BOTH, expand=1)
        self.menu()
        self.root.title('Project 1')
        Label(self.frame,text='Welcome back!',font=('Helvetica',32),pady=100).pack()
        self.frame.pack()
    def start(self):
        self.root.mainloop()

    def menu(self):
        menu = Menu(self.root)
        menu.add_command(label='Train Model',command = self.train)
        menu.add_command(label='Show Parameters')
        menu.add_command(label='Live Predictions')
        menu.add_command(label='Save')
        menu.add_command(label="Load")
        menu.add_command(label='About')
        self.root.config(menu=menu)
        self.frame.pack()

    def clean(self):
        for i in self.frame.winfo_children():
            i.destroy()

    def train(self):
        self.file = ''
        self.clean()
        text= StringVar()
        tmp = Label(self.frame,text='Pick training dataset',font=('Helvetica',18))
        tmp.place(x=(self.frame.winfo_width()/2),y=20, anchor='center')
        Label(self.frame,textvariable=text).place(x=30,y=200)
        Button(self.frame,text='Select file', command= lambda: [self.fileOpen(text)]).place(x=self.frame.winfo_width()/2+100, y=200)
        Button(self.frame, text='Start training session', command= self.startTrain).place(x= self.frame.winfo_width()/2,y=250, anchor='center')

    def startTrain(self):
        pass

    def fileOpen(self,text):
        text.set(filedialog.askopenfilename(initialdir="", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*"))))

gui = GUI()
gui.start()
