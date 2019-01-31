from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
class GUI:

    def __init__(self):
        self.root = Tk()
        self.root.geometry('1000x650')
        self.root.resizable(False,False)
        self.root.iconbitmap(r'c:\Users\Jakubko\PycharmProjects\Projekt123\GUI\brain-favicon.ico')
        self.frame = Frame(self.root, bg='white')
        self.frame.pack(fill=BOTH,expand=1)
        self.menu()
        self.root.title('Project 1')
        Label(self.frame,text='Welcome back!',font=('Helvetica',32),pady=100,bg='white').pack()
        self.frame.pack()
    def start(self):
        self.root.mainloop()

    def menu(self):
        menu = Menu(self.root)

        menuDropdown = Menu(menu)
        menuDropdown.add_command(label='Load Model')

        modelMenu = Menu(menu)
        modelMenu.add_command(label='Show Model',command=self.showParameters)
        modelMenu.add_command(label='Model Structure')
        modelMenu.add_command(label='Training Session')
        modelMenu.add_command(label='Training Video')
        modelMenu.add_command(label='About Model')


        datasetMenu = Menu(menu)
        datasetMenu.add_command(label='Show Training Dataset',command=self.showDataset)
        datasetMenu.add_command(label='Show Test Dataset',command=self.showDataset)

        helpMenu = Menu(menu)
        helpMenu.add_command(label='Article')
        helpMenu.add_command(label='Contributors')

        menu.add_cascade(label='Menu',menu=menuDropdown)
        menu.add_cascade(label='Model',menu= modelMenu)
        menu.add_command(label='Live Predictions')
        menu.add_cascade(label='Datasets',menu=datasetMenu)
        menu.add_cascade(label='Help',menu= helpMenu)
        menu.add_command(label='About')
        self.root.config(menu=menu)
        self.frame.pack()

    def clean(self):
        for i in self.frame.winfo_children():
            i.destroy()

    def showDataset(self,data,labels,predicted_labels):
        # self.file = ''
        # self.clean()
        # text= StringVar()
        # tmp = Label(self.frame,text='Datasets',bg='white',font=('Helvetica',18))
        # tmp.place(x=(self.frame.winfo_width()/2),y=20, anchor='center')
        # Label(self.frame,textvariable=text,bg='white').place(x=30,y=200)
        # Button(self.frame,text='Select dataset', command= lambda: [self.fileOpen(text)]).place(x=self.frame.winfo_width()/2+100, y=200)
        # Button(self.frame, text='Start presentation', command= self.startTrain).place(x= self.frame.winfo_width()/2,y=250, anchor='center')

        figure = plt.figure(figsize=(10, 10))
        i = 1
        ax = []  # na manipulaciu subloptmi
        index = 0
        for img in data:
            if (index < 4):  ## test
                # img = np.random.randint(10, size=(10, 10))
                figure.add_subplot(2, 2, i)
                ax.append(figure.add_subplot(2, 2, i))
                color = 'red'
                if (labels[i - 1] == predicted_labels[i - 1]):
                    color = 'green'
                ax[i - 1].set_title('Real:{} Pred:{}'.format(labels[i - 1], int(predicted_labels[i - 1])), color=color)
                plt.imshow(img)
                i += 1
                index += 1
        canvas = FigureCanvasTkAgg(figure, self.frame)
        canvas.get_tk_widget().pack(fill=BOTH,expand=1)

    def startTrain(self):
        pass

    def fileOpen(self,text):
        text.set(filedialog.askopenfilename(initialdir="", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*"))))
    def showParameters(self):
        self.clean()
        labels=['Accuracy: ','Specificity: ','Sensitivity: ','MAPE(train): ','MAPE(test): ']
        values=[68,72,48,72,65]
        Label(self.frame, text='Model Parameters',bg='white', font=('Helvetica',18)).place(x=self.frame.winfo_width()/2,y=20,anchor='center')
        for i in range(5):
            Label(self.frame,text=labels[i],bg='white').place(x=100,y=100 + i * 30,anchor='e')
            Label(self.frame, text=(str(values[i]) + '%' if i > 2 else str(values[i])) ,bg='white' ).place(x=150, y=100 + i * 30, anchor='e')
        figure = plt.Figure(figsize=(7,5),dpi=100)
        ax = figure.add_subplot(111)
        ax.xaxis.label.set_visible(False)
        canvas = FigureCanvasTkAgg(figure,self.frame)
        data1 = {'Epoch': [0, 120, 240, 300, 400, 450, 500, 550, 600, 650],
                 'Error': [0.9, 0.6, 0.3, 0.25, 0.23, 0.2, 0.18, 0.15,0.14, 0.14]
                 }
        df = DataFrame(data=data1,columns=['Epoch','Error'])
        df = df[['Epoch','Error']].groupby('Epoch').sum()
        canvas.get_tk_widget().pack(side=RIGHT)
        df.plot(kind='line',ax=ax)

gui = GUI()
gui.start()
