import os

path = 'dataset/cnn/'

# rozdelenie celeho setu na zlozky podla diagnoz
def split_image_by_diagnoses():
    with open(path+'/description(10015)/metadata_with_X.csv', 'r') as metadata:
        #os.mkdir(path+'processed')
        #os.mkdir(path+'processed/malignant')
        #os.mkdir(path+'processed/benign')
        #os.mkdir(path+'processed/unclassed')     ## pre tie co nemaju diagnozu
        map = ['benign/','malignant/']
        for line in metadata:
            data = line.split(';')
            with open(path+'/images/'+data[0], 'rb') as file:
                filedata = file.read()
                with open(path+'/processed/'+map[int(data[1])]+ data[0], 'wb') as newfile:
                    newfile.write(filedata)
                    newfile.close()
                file.close()
            os.remove(path+'images/'+data[0])

# rozdelenie processed obrazkov na podtriedy
def split_images_into_sets():
    os.mkdir(path + 'train')
    os.mkdir(path + 'train/malignant')
    os.mkdir(path + 'train/benign')
    os.mkdir(path + 'test')
    os.mkdir(path + 'test/malignant')
    os.mkdir(path + 'test/benign')
    os.mkdir(path + 'validation')
    os.mkdir(path + 'validation/malignant')
    os.mkdir(path + 'validation/benign')

if __name__ == '__main__':
    split_image_by_diagnoses()