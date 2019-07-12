import math

## global params
theta = - math.pi / 8
ratio = 0.7
bounding_box_margin = 10
inter_layer_margin = 50
text_margin = 50
channel_scale = 0.5
text_size = 10
one_dim_width = 20
line_color_feature_map = (0, 0, 0)
line_color_layer = (0, 0, 255)
text_color_feature_map = (0, 0, 0)
text_color_layer = (0, 0, 0)

## netwok params
IMG_SIZE_X = 64 #450
IMG_SIZE_Y = 64 #300
EPOCH = 10
TRAIN_DATA = 80
TEST_DATA = 20
learning_coef = 0.01 #0.001

##program params
load_model = False   # TRUE trenuje novy model
				# False nacita loadnuty
initializer_seed = None
threshold = 0.4999
