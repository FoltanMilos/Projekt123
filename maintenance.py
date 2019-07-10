import os


path = 'dataset/tmp/'

with open(path+'/description/metadata.csv', 'r') as metadata:
    os.mkdir(path+'processed')
    os.mkdir(path+'processed/malignant')
    os.mkdir(path+'processed/benign')
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
