## netwok params
IMG_SIZE_X = 64 #450
IMG_SIZE_Y = 64 #300
EPOCH = 10
TRAIN_DATA = 80
TEST_DATA = 20
learning_coef = 0.01 ## nie je treba pri ADADELTE

# datasety  - absolutne cisla
# spolu 10015   - Ben[6705] malig[1113] neurcene[2197]
# urcene -7818-
# na sety: 		Train[]   Test[]    Valid[]
train_ratio = 6000  #76.75
count_train_malig = 854
count_train_benign = 5146
valid_ratio = 1000   #12.8
count_valid_malig = 142
count_valid_benign = 858
test_ratio = 818
count_test_malig = 117
count_test_benign = 701

##program params
load_model = False   # TRUE trenuje novy model
				# False nacita loadnuty
initializer_seed = None
threshold = 0.4999


## kym nie je db - cesty TEST
path_train = 'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\train\\'
path_test = 'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\test\\'
path_validation = 'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\validation\\'