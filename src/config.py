IMG_SIZE_X = 64 #450
IMG_SIZE_Y = 64 #300
EPOCH = 10
TRAIN_DATA = 80
TEST_DATA = 20
learning_coef = 0.01 ## nie je treba pri ADADELTE

train_ratio = 6000  #76.75
count_train_malig = 854
count_train_benign = 5146
valid_ratio = 1000   #12.8
count_valid_malig = 142
count_valid_benign = 858
test_ratio = 818
count_test_malig = 117
count_test_benign = 701

				# False nacita loadnuty
initializer_seed = None
threshold = 0.4999

# server
server_host = 0000
server_port = 8000

## kym nie je db - cesty TEST
path_train = 'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\main_dataset\\train\\'
path_test = 'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\main_dataset\\test\\'
path_validation = 'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\main_dataset\\validation\\'