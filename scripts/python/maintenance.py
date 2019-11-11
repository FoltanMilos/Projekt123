import os
import config as conf
import glob

path = 'dataset/main_dataset'
img_format = '.jpg'
ratio_index = 0

# rozdelenie celeho setu na zlozky podla diagnoz
def split_image_by_diagnoses():
    with open(path+'/description(10015)/metadata_with_X.csv', 'r',encoding='UTF-8') as metadata:
        map = ['benign/','malignant/','unclassed/']
        for line in metadata:
            data = line.split(';')
            with open(path+'/images(10015)/'+data[0]+img_format, 'rb') as file:
                filedata = file.read()
                # priradenie do datasetu podla ratia
                with open(path+'/processed/'+map[int(data[1])]+data[0]+img_format, 'wb') as newfile:
                    newfile.write(filedata)
                    newfile.close()
                file.close()
            os.remove(path+'/images(10015)/'+data[0]+img_format)

def create_dirs():
    os.mkdir(path + '/train')
    os.mkdir(path + '/train/malignant')
    os.mkdir(path + '/train/benign')
    os.mkdir(path + '/test')
    os.mkdir(path + '/test/malignant')
    os.mkdir(path + '/test/benign')
    os.mkdir(path + '/validation')
    os.mkdir(path + '/validation/malignant')
    os.mkdir(path + '/validation/benign')

def create_sets():
    map_ratio = ['train/', 'validation/', 'test/']
    map = ['benign/', 'malignant/', 'unclassed/']
    ratio_index = 0
    # benigns setting
    print_path = ''
    print_max = 0
    p_index = 0
    for img_path in glob.iglob("dataset/main_dataset/processed/benign/*.jpg"):
        with open(img_path, 'rb') as file:
            filedata = file.read()
            if(ratio_index <= conf.count_train_benign):
                with open(path + '/train/benign/' + img_path.split("\\")[1], 'wb') as newfile: #win
                # linux with open(path + '/train/benign/'+img_path.split("/")[-1] , 'wb') as newfile:
                    print_path = '/train/benign/'
                    p_index = ratio_index
                    print_max = conf.count_train_benign
                    newfile.write(filedata)
                    newfile.close()
            elif(ratio_index - conf.count_train_benign <= conf.count_valid_benign):
                with open(path + '/validation/benign/' + img_path.split("\\")[1], 'wb') as newfile: #win
                    #linux with open(path + '/validation/benign/' + img_path.split("/")[-1], 'wb') as newfile:
                    print_path = '/validation/benign/'
                    p_index =ratio_index - conf.count_train_benign
                    print_max = conf.count_valid_benign
                    newfile.write(filedata)
                    newfile.close()
            elif(ratio_index  - conf.count_train_benign -conf.count_valid_benign <= conf.count_test_benign):
                with open(path + '/test/benign/' + img_path.split("\\")[1], 'wb') as newfile: #win
                #linux with open(path + '/test/benign/' + img_path.split("/")[-1], 'wb') as newfile:
                    print_path = '/test/benign/'
                    p_index = ratio_index  - conf.count_train_benign -conf.count_valid_benign
                    print_max = conf.count_test_benign
                    newfile.write(filedata)
                    newfile.close()
            file.close()
        print("["+str(p_index)+"/"+ str(print_max)+"] - " + img_path.split("\\")[1] + " -> " + print_path) #win
        #linux print("["+str(p_index)+"/"+ str(print_max)+"] - " + img_path.split("/")[-1] + " -> " + print_path)
        ratio_index = ratio_index +1

    # malignants setting
    ratio_index = 0
    print("---------------MALIG----------------------")
    for img_path in glob.iglob("dataset/main_dataset/processed/malignant/*.jpg"):
        with open(img_path, 'rb') as file:
            filedata = file.read()
            if(ratio_index <= conf.count_train_malig):
                with open(path + '/train/malignant/' + img_path.split("\\")[1], 'wb') as newfile: #win
                    #linux with open(path + '/train/malignant/'+img_path.split("/")[-1] , 'wb') as newfile:
                    print_path = '/train/malignant/'
                    p_index = ratio_index
                    print_max = conf.count_train_malig
                    newfile.write(filedata)
                    newfile.close()
            elif(ratio_index-conf.count_train_malig <= conf.count_valid_malig):
                with open(path + '/validation/malignant/' + img_path.split("\\")[1], 'wb') as newfile: #win
                    #linux with open(path + '/validation/malignant/' + img_path.split("/")[-1], 'wb') as newfile:
                    print_path = '/validation/malignant/'
                    p_index = ratio_index-conf.count_train_malig
                    print_max = conf.count_valid_malig
                    newfile.write(filedata)
                    newfile.close()
            elif(ratio_index -conf.count_valid_malig-conf.count_train_malig<= conf.count_test_malig):
                with open(path + '/test/malignant/' + img_path.split("/")[-1], 'wb') as newfile:
                    print_path = '/test/malignant/'
                    p_index = ratio_index -conf.count_valid_malig-conf.count_train_malig
                    print_max = conf.count_test_malig
                    newfile.write(filedata)
                    newfile.close()
            file.close()
        print("[" + str(p_index) +"/" + str(print_max) + "] - " + img_path.split("\\")[1] + " -> " + print_path) #win
        #linux print("[" + str(p_index) +"/" + str(print_max) + "] - " + img_path.split("/")[-1] + " -> " + print_path)
        ratio_index = ratio_index +1


if __name__ == '__main__':
    # skopni si vsetky fotky do zlozky images(10015) a description(10015) pouzi uyprave
    # odkomentuj metody a pusti

    # split_image_by_diagnoses()
    # create_dirs()
    #create_sets()
    print('end')