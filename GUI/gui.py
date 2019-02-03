from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
import data
from PIL import Image,ImageTk
import os

class GUI:
    def __init__(self):
        self.data =data.Data()
        self.data.load_all_data()
        self.data.load_all_labels()
        self.root = Tk()
        self.root.geometry('1000x650')
        self.root.resizable(False,False)
        self.root.iconbitmap(r'GUI\brain-favicon.ico')
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
        menuDropdown.add_command(label='Load Your Model...')
        menuDropdown.add_command(label='Exit')

        modelMenu = Menu(menu)
        modelMenu.add_command(label='Show Model')
        modelMenu.add_command(label='Model Structure')
        modelMenu.add_command(label='Training Session',command=self.showParameters)
        modelMenu.add_command(label='Training Video')



        datasetMenu = Menu(menu)
        datasetMenu.add_command(label='Show Training Dataset',command=lambda: self.showDataset(False,0))
        datasetMenu.add_command(label='Show Test Dataset',command= lambda: self.showDataset(True,0))
        datasetMenu.add_command(label='Dataset Information')  ## tu daj vypis ze z kade mame foto

        helpMenu = Menu(menu)
        helpMenu.add_command(label='Tutorial')

        livePred = Menu(menu)
        livePred.add_command(label='Chcek Your Photo...',command=self.loadPhoto)
        livePred.add_command(label='Load Example Photo...',command= self.loadExamplePhoto)

        aboutMenu = Menu(menu)
        aboutMenu.add_command(label='Article')
        aboutMenu.add_command(label='Contributors',command=self.aboutContributors)
        aboutMenu.add_command(label='Our work',command=self.about)
        aboutMenu.add_command(label='Model know-how')

        menu.add_cascade(label='Menu',menu=menuDropdown)
        menu.add_cascade(label='Model',menu= modelMenu)
        menu.add_cascade(label='Live Predictions',menu=livePred)
        menu.add_cascade(label='Datasets',menu=datasetMenu)
        menu.add_cascade(label='Help',menu= helpMenu)
        menu.add_cascade(label='About',menu=aboutMenu,)
        self.root.config(menu=menu)
        self.frame.pack()

    def clean(self):
        for i in self.frame.winfo_children():
            i.destroy()


    def showDataset(self,test ,page = 0,first=True):
        # self.file = ''
        # self.clean()
        # text= StringVar()
        # tmp = Label(self.frame,text='Datasets',bg='white',font=('Helvetica',18))
        # tmp.place(x=(self.frame.winfo_width()/2),y=20, anchor='center')
        # Label(self.frame,textvariable=text,bg='white').place(x=30,y=200)
        # Button(self.frame,text='Select dataset', command= lambda: [self.fileOpen(text)]).place(x=self.frame.winfo_width()/2+100, y=200)
        # Button(self.frame, text='Start presentation', command= self.startTrain).place(x= self.frame.winfo_width()/2,y=250, anchor='center')
        self.clean()
        figure = plt.figure(figsize=(10, 10))
        i = 1
        ax = []  # na manipulaciu subloptmi
        if test == True:
            dataset = self.data.test_data
            labels = self.data.test_labels
        else:
            dataset = self.data.train_data
            labels = self.data.train_labels

        for img in range(page*4,page*4 + min(4,dataset.__len__() - page*4)):
            ## test
            # img = np.random.randint(10, size=(10, 10))
            # figure.add_subplot(2, 2, i)
            tmp = figure.add_subplot(2, 2, i)
            tmp.xaxis.set_visible(False)
            tmp.yaxis.set_visible(False)
            ax.append(tmp)

            color = 'red'
            print(img)
            ax[divmod(img,4)[1]].set_title('Malignant:{}'.format(labels[img], color='black'))
            plt.imshow(dataset[img])
            i += 1
        canvas = FigureCanvasTkAgg(figure, self.frame)
        canvas.get_tk_widget().pack(fill=BOTH,expand=1)
        if ((page+1)*4 <= dataset.__len__()):
            Button(self.frame,text='>',font=('helvetica',24),bg='white',command= lambda: [plt.close('all'),canvas.get_tk_widget().destroy(),self.showDataset(test,page + 1,False)])\
            .place(x=self.frame.winfo_width()-100,y=self.frame.winfo_height()/2)
        if page + 1*4 > 4:
            Button(self.frame, text='<',font=('helvetica',24),bg='white',command=lambda: [plt.close('all'),canvas.get_tk_widget().pack_forget(),canvas.get_tk_widget().destroy(),self.showDataset(test,page -1,False)]) \
            .place(x=50, y=self.frame.winfo_height()/2 )


    def startTrain(self):
        pass

    def fileOpen(self,text):
        text.set(filedialog.askopenfilename(initialdir=os.path.dirname(os.path.realpath('data/images/')), title="Select file",
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

    def about(self):
        self.clean()
        Label(self.frame,text="Our Work",font=('Helvetica',18)).place(x=self.frame.winfo_width()/2,anchor=CENTER,y=20)
        text = Text(self.frame,width=95,height=30)
        scroll = Scrollbar(self.frame, command = text.yview)
        content = """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vulputate tellus metus, at maximus nunc tincidunt in. Suspendisse blandit, felis eget sollicitudin condimentum, magna nisi interdum nisi, vel sodales arcu turpis eu libero. Nulla iaculis mauris eget dapibus ullamcorper. Ut molestie velit nec sem pretium porttitor. Sed finibus sit amet lectus eu blandit. Donec rhoncus sollicitudin velit in tristique. Donec luctus tortor tellus, vitae vehicula arcu rutrum nec. Mauris porttitor sed nunc vel mollis. Nulla hendrerit ex pellentesque tortor rhoncus elementum. Ut sed finibus felis. Fusce aliquam pretium erat, vel pellentesque tortor blandit ac. Etiam euismod aliquam dolor, nec feugiat quam blandit vitae. Integer egestas massa eros, mattis dictum velit luctus vel. Suspendisse aliquet posuere quam, sit amet scelerisque est dapibus posuere. Integer non dui eu velit tincidunt consectetur sit amet eu eros.

            Integer tempor dapibus turpis, id facilisis dolor efficitur nec. In dignissim sem quis nisl condimentum malesuada. Etiam tempor egestas tellus, id scelerisque nisi pellentesque quis. Sed facilisis sodales velit, id fringilla sapien tempus nec. Proin at luctus leo. Sed elementum orci sed est pharetra auctor. Sed eleifend varius orci sodales viverra. Vivamus id maximus libero, eu porttitor velit. Phasellus vel cursus neque. Sed et dignissim velit. Vestibulum eu sodales urna, eu ornare lorem.

            Donec egestas placerat turpis, ac hendrerit felis tincidunt a. Etiam ac est consectetur, suscipit risus nec, congue nibh. Nulla elit odio, tincidunt a orci et, condimentum fringilla ex. Proin eleifend bibendum ullamcorper. Phasellus pretium libero egestas tempus sagittis. Nullam vel purus ut lorem consectetur suscipit. Curabitur fringilla, leo non consequat facilisis, dolor nisi condimentum lorem, vitae malesuada lectus odio porttitor eros. Nam placerat pharetra risus id aliquet. Nullam luctus justo aliquet, tincidunt erat vel, tristique risus. In metus nunc, commodo non volutpat vel, sodales id dolor. Phasellus auctor, ex quis semper porttitor, risus ex interdum urna, ut auctor leo magna non mi. Integer vitae mollis ex.

            Cras pulvinar vehicula nisl, sed fermentum enim convallis et. Vestibulum a cursus quam. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Mauris justo massa, malesuada sit amet laoreet nec, aliquam at magna. Sed non pretium dolor, a dictum diam. Sed eget augue velit. Curabitur eu laoreet diam. Fusce quis leo sapien. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris elementum porttitor eros at mattis. Nunc accumsan velit nisi, eget hendrerit turpis aliquet vel. Etiam imperdiet euismod sapien, ac fermentum nisl dapibus ac. Duis quis eros risus. In metus nulla, pretium et neque a, vulputate vehicula orci.

            Aenean id tortor imperdiet, ultrices diam ac, semper tellus. Mauris id imperdiet arcu. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Proin sollicitudin sollicitudin bibendum. Curabitur in vehicula est. Aenean consectetur tincidunt odio vitae pretium. Morbi convallis ante id augue mattis, at ultrices tellus suscipit. Donec hendrerit leo sit amet commodo scelerisque. Phasellus vitae arcu sit amet tortor hendrerit molestie. Nullam id molestie felis. Morbi non commodo odio. Duis blandit augue tincidunt, accumsan enim eu, fringilla diam. Cras ac felis ipsum. Aliquam erat volutpat. Nam vitae sapien ut magna egestas auctor sit amet vel justo. Sed a erat erat."""
        text.insert(END,content)
        text.config(state=DISABLED)
        text.configure(yscrollcommand=scroll.set, borderwidth=0)
        scroll.pack(fill=Y,side=RIGHT)
        text.place(x=200,y=100)

    def loadExamplePhoto(self):
        self.clean()
        frame = Frame(self.frame,width=330,height=self.frame.winfo_height()-40)
        text = Text(frame,width=40,height=30)
        scrollbar = Scrollbar(frame,command = text.yview())
        content = """
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vulputate tellus metus, at maximus nunc tincidunt in. Suspendisse blandit, felis eget sollicitudin condimentum, magna nisi interdum nisi, vel sodales arcu turpis eu libero. Nulla iaculis mauris eget dapibus ullamcorper. Ut molestie velit nec sem pretium porttitor. Sed finibus sit amet lectus eu blandit. Donec rhoncus sollicitudin velit in tristique. Donec luctus tortor tellus, vitae vehicula arcu rutrum nec. Mauris porttitor sed nunc vel mollis. Nulla hendrerit ex pellentesque tortor rhoncus elementum. Ut sed finibus felis. Fusce aliquam pretium erat, vel pellentesque tortor blandit ac. Etiam euismod aliquam dolor, nec feugiat quam blandit vitae. Integer egestas massa eros, mattis dictum velit luctus vel. Suspendisse aliquet posuere quam, sit amet scelerisque est dapibus posuere. Integer non dui eu velit tincidunt consectetur sit amet eu eros.
                """
        text.insert(END,content)
        text.config(state = DISABLED,yscrollcommand=scrollbar.set,borderwidth=0)
        scrollbar.pack(fill=Y,side=RIGHT)
        text.pack(fill=Y,side=LEFT)
        Label(self.frame,text='Description', font=('Helvetica',18),bg='white').place(x=130,y=20)
        Label(self.frame,text='Select example photo', font=('Helvetica',18),bg='white').place(x=600,y=20)
        textvar = StringVar()
        textvar.set('')
        frame.place(x=0,y=40)
        Label(self.frame,textvariable=textvar , bg='white').place(x=400,y=200)
        Button(self.frame,text='Select',command=lambda: self.fileOpen(textvar)).place(x=900,y=200)
        Button(self.frame,text='Evaluate photo').place(x=650,y=300)

    def aboutContributors(self):
        self.clean()
        photos = ['trololo.jpg', 'trololo.jpg', 'trololo.jpg', 'trololo.jpg', 'trololo.jpg']
        content = ['Milos', 'Ja', 'Mato', 'Stevo', 'Filip']
        for i in range(photos.__len__()):
            if (i % 2 == 1):
                text = Text(self.frame, width=80, height=4,borderwidth=1)
                text.insert(END, content[i])
                text.configure(state=DISABLED)
                text.place(x=80, y=100 * i + 20)
                img = Image.open('tmp.gif')
                img = ImageTk.PhotoImage(img)
                panel = Label(self.frame, image=img,width=80 , height=80)
                panel.image = img
                panel.place(x=800,y=100*i+20)
            else:
                text = Text(self.frame, width=80, height=4,borderwidth=1)
                text.insert(END, content[i])
                text.configure(state=DISABLED)
                text.place(x=280, y=100 * i + 20)
                img = Image.open('tmp.gif')
                img = ImageTk.PhotoImage(img)
                panel = Label(self.frame, image=img,width=80 , height=80)
                panel.image = img
                panel.place(x=80, y=100 * i + 20)

    def loadPhoto(self):
        self.clean()
        Label(self.frame,text='Live Prediction',font=('helvetica',18),bg='white').place(x=self.frame.winfo_width()/2,y=20,anchor=CENTER)
        text= StringVar()
        Button(self.frame, text='Select Photo', command=lambda:  self.fileOpen(text)).place(x=750,y=100)
        Label(self.frame,textvariable=text,bg='white').place(x=200,y=100)
        Button(self.frame,text='Evaluate Photo',command=lambda: self.evaluate(text.get())).place(x=self.frame.winfo_width()/2,y=300,anchor=CENTER)

    def evaluate(self,path):
        self.clean()
        Label(self.frame,text='Live Prediction',font=('helvetica',18),bg='white').place(x=self.frame.winfo_width()/2,y=20,anchor=CENTER)
        Label(self.frame,text='Verdict',bg='white').place(x=50,y=60)
        verdict = StringVar()
        verdict.set('OK')
        Label(self.frame,textvariable=verdict,bg='white').place(x=70,y=80)
        Label(self.frame,text='Recommendation').place(x=50,y=150)
        content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vulputate tellus metus, at maximus nunc tincidunt in. Suspendisse blandit, felis eget sollicitudin condimentum, magna nisi interdum nisi, vel sodales arcu turpis eu libero. Nulla iaculis mauris eget dapibus ullamcorper. Ut molestie velit nec sem pretium porttitor. Sed finibus sit amet lectus eu blandit. Donec rhoncus sollicitudin velit in tristique. Donec luctus tortor tellus, vitae vehicula arcu rutrum nec. Mauris porttitor sed nunc vel mollis. Nulla hendrerit ex pellentesque tortor rhoncus elementum. Ut sed finibus felis. Fusce aliquam pretium erat, vel pellentesque tortor blandit ac. Etiam euismod aliquam dolor, nec feugiat quam blandit vitae. Integer egestas massa eros, mattis dictum velit luctus vel. Suspendisse aliquet posuere quam, sit amet scelerisque est dapibus posuere. Integer non dui eu velit tincidunt consectetur sit amet eu eros."
        txt = Text(self.frame,width=30,height=15,borderwidth=0)
        txt.insert(END,content)
        txt.configure(state=DISABLED)
        txt.place(x=50,y=170)
        img = Image.open(path)
        img = ImageTk.PhotoImage(img)
        panel = Label(self.frame, image = img)
        panel.image = img
        panel.place(x=350,y=100)



if __name__ == "__main__":
    gui = GUI()
    gui.start()

