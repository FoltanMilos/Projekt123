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
import backend as bck
from keras.utils import plot_model
from matplotlib_util import save_model_to_file
from convnet_drawer import Model, Conv2D, MaxPooling2D, Flatten, Dense, config
import matplotlib.pyplot as plt
import configuration as conf
import csv

class GUI:
    ## na oddelenie gui od ostatku app
    # obsahuje
    #       - data_train
    #       - data_test
    #       - model
    global backend

    def __init__(self):
        #INIT backend
        self.backend = bck.Backend(False)

        #gui init
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
        menuDropdown.add_command(label='Load Your Model...',state=DISABLED)
        menuDropdown.add_command(label='Exit',command=exit)

        modelMenu = Menu(menu)
        #modelMenu.add_command(label='Show Model')
        modelMenu.add_command(label='Model Structure',command=self.showModelStructure)
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
            dataset = self.backend.data.test_data
            labels = self.backend.data.test_labels
        else:
            dataset = self.backend.data.train_data
            labels = self.backend.data.train_labels

        for img in range(page*4,page*4 + min(4,dataset.__len__() - page*4)):
            tmp = figure.add_subplot(2, 2, i)
            tmp.xaxis.set_visible(False)
            tmp.yaxis.set_visible(False)
            ax.append(tmp)

            color = 'red'
            #print(img)
            result = ""
            if(test):
                # je to testovanie tak aj opredikovane veci
                result = self.backend.model.predict_image(dataset[img]) #,labels[img]
                if(int(str(result).split("[")[2].split("]")[0].split(".")[0]) == 1):
                    result = "Malignant"
                else:
                    result = "OK"
            else:
                pass

            label = 'Malignant' if int(labels[img]) == 0 else "OK"
            ax[divmod(img,4)[1]].set_title('Real diagnosis: {} \n Predicted diagnosis: {}'.format(label,result, color='black'))
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
        path = self.loadPhoto()

        # to iste, len k tomu uz bude nahrana diagnoza
        realDiagnosis = StringVar()
        with open('obrazkyIne/description(MSK-1)/metadata.csv', 'r') as csvfile:
            subor = csv.reader(csvfile, delimiter=';')
            for i in subor:
                if(str(i[0]) == str(path).split("\.")[0].split("/")[str(path).split("/").__len__()-1].split(".")[0]):
                    if(int(i[1]) == 1):
                        realDiagnosis.set("Malignant")
                        break
                    else:
                        realDiagnosis.set("OK")
                        break

        Label(self.frame, text='Real diagnosis', font=('helvetica', 14)).place(x=50, y=160)
        Label(self.frame, textvariable=realDiagnosis, bg='white', font=('helvetica', 12)).place(x=70, y=200)


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
        #Label(self.frame,text='Live Prediction',font=('helvetica',18),bg='white').place(x=self.frame.winfo_width()/2,y=20,anchor=CENTER)
        text= StringVar()
        #Button(self.frame, text='Select Photo', command=lambda:
        self.fileOpen(text) #).place(x=750,y=100)

        # nahra fotku z vybranej cesty
        #img = self.backend.data.load_solo_img(text.get())
        self.evaluate(text.get())
        #Label(self.frame,textvariable=text,bg='white').place(x=200,y=100)
        #Button(self.frame,text='Evaluate Photo',command=lambda: self.evaluate(text.get())).place(x=self.frame.winfo_width()/2,y=300,anchor=CENTER)
        return text.get()

    def evaluate(self,path):
        self.clean()
        #predikcia seiete

        img = Image.open(path)
        img = img.resize((conf.IMG_SIZE_Y, conf.IMG_SIZE_X), Image.ANTIALIAS)
        result = self.backend.model.predict_image(img)
        if(int(str(result).split("[")[2].split("]")[0].split(".")[0]) == 1):
            result = "Malignant appearance"
        else:
            result = "No positive match "
        img = ImageTk.PhotoImage(img)
        verdict = StringVar()
        verdict.set(str(result))

        Label(self.frame,text='Prediction',font=('helvetica',18),bg='white').place(x=self.frame.winfo_width()/2,y=50,anchor=CENTER)
        Label(self.frame,text='Verdict',font=('helvetica',14)).place(x=50,y=60)
        Label(self.frame,textvariable=verdict,bg='white',font=('helvetica',12)).place(x=70,y=100)
        Label(self.frame,text='Recommendation',font=('helvetica',14)).place(x=50,y=270)
        content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vulputate tellus metus, at maximus nunc tincidunt in. Suspendisse blandit, felis eget sollicitudin condimentum, magna nisi interdum nisi, vel sodales arcu turpis eu libero. Nulla iaculis mauris eget dapibus ullamcorper. Ut molestie velit nec sem pretium porttitor. Sed finibus sit amet lectus eu blandit. Donec rhoncus sollicitudin velit in tristique. Donec luctus tortor tellus, vitae vehicula arcu rutrum nec. Mauris porttitor sed nunc vel mollis. Nulla hendrerit ex pellentesque tortor rhoncus elementum. Ut sed finibus felis. Fusce aliquam pretium erat, vel pellentesque tortor blandit ac. Etiam euismod aliquam dolor, nec feugiat quam blandit vitae. Integer egestas massa eros, mattis dictum velit luctus vel. Suspendisse aliquet posuere quam, sit amet scelerisque est dapibus posuere. Integer non dui eu velit tincidunt consectetur sit amet eu eros."
        txt = Text(self.frame,width=30,height=15,borderwidth=0)
        txt.insert(END,content)
        txt.configure(state=DISABLED)
        txt.place(x=50,y=300)
        panel = Label(self.frame, image = img)
        panel.image = img
        panel.place(x=350,y=100)

    def showModelStructure(self):
        self.clean()
        text = Text(self.frame, width=95, height=30)
        scroll = Scrollbar(self.frame, command=text.yview)
        content = ""  #str(self.backend.model.model.to_json())
        text.insert(END, content)
        text.config(state=DISABLED)
        text.configure(yscrollcommand=scroll.set, borderwidth=0)
        scroll.pack(fill=Y, side=RIGHT)
        text.place(x=200, y=100)

        model = Model(input_shape=(450, 600, 3))
        model.add(Conv2D(32, (11, 11), ))
        model.add(MaxPooling2D((2, 2), ))
        model.add(Conv2D(32, (11, 11), ))
        model.add(MaxPooling2D((2, 2), ))
        model.add(Flatten())
        model.add(Dense(1))
        save_model_to_file(model, "example.pdf")


        img = Image.open('GUI/modelStructure.png')
        img = img.resize((conf.IMG_SIZE_Y, conf.IMG_SIZE_X), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(self.frame, image=img)
        panel.image = img
        panel.place(x=350, y=100)

        #uprava frame
        Label(self.frame, text='Model structure', font=('helvetica', 18), bg='white').place(x=self.frame.winfo_width() / 2,
                                                                                   y=50, anchor=CENTER)
        inputDense = StringVar()
        inputDense.set("Input dense")
        Label(self.frame, text='Input dense', font=('helvetica', 14)).place(x=50, y=60)
        Label(self.frame, textvariable=inputDense, bg='white', font=('helvetica', 12)).place(x=70, y=100)

        hiddenDenses = StringVar()
        hiddenDenses.set("Hiden dense 1")
        Label(self.frame, text='Hidden denses', font=('helvetica', 14)).place(x=50, y=160)
        Label(self.frame, textvariable=hiddenDenses, bg='white', font=('helvetica', 12)).place(x=70, y=200)
        Label(self.frame, textvariable=hiddenDenses, bg='white', font=('helvetica', 10)).place(x=70, y=220)

        Label(self.frame, textvariable=hiddenDenses, bg='white', font=('helvetica', 12)).place(x=70, y=250)
        Label(self.frame, textvariable=hiddenDenses, bg='white', font=('helvetica', 10)).place(x=70, y=270)

        Label(self.frame, textvariable=hiddenDenses, bg='white', font=('helvetica', 12)).place(x=70, y=300)
        Label(self.frame, textvariable=hiddenDenses, bg='white', font=('helvetica', 10)).place(x=70, y=320)

        Label(self.frame, textvariable=hiddenDenses, bg='white', font=('helvetica', 12)).place(x=70, y=350)
        Label(self.frame, textvariable=hiddenDenses, bg='white', font=('helvetica', 10)).place(x=70, y=370)

        output = StringVar()
        hiddenDenses.set("Output dense")
        Label(self.frame, text='Ouput dense', font=('helvetica', 14)).place(x=50, y=430)
        Label(self.frame, textvariable=hiddenDenses, bg='white', font=('helvetica', 12)).place(x=70, y=470)


if __name__ == "__main__":
    gui = GUI()
    gui.start()

