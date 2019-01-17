import matplotlib.pyplot as plt
import numpy as np

class Plot_modified:

    # plotne obrazky v liste
    # k nim priradi ich urcenu hodnotu REAL --> labels
    # porovna s hodnotou predikcii daneho labelu
        # --> pustitelne len na batch hodnoty, pre jeden obrazok treba upravu kodu metody, nepusti asi kompilator
    def plot_data(self,data,labels,predicted_labels):
        figure = plt.figure(figsize=(10,10))
        i = 1
        ax = [] # na manipulaciu subloptmi
        for img in data:
            #img = np.random.randint(10, size=(10, 10))
            figure.add_subplot(2,2 , i)
            ax.append(figure.add_subplot(2,2,i))
            color = 'red'
            if(labels[i-1] == predicted_labels[i-1]):
                color = 'green'
            ax[i-1].set_title('Real:{} Pred:{}'.format(labels[i-1],int(predicted_labels[i-1])),color=color)
            plt.imshow(img)
            i+=1
        plt.show(block=True)