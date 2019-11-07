import keras.callbacks as ker_clbck


class LiveLearningCallback(ker_clbck.Callback):
	def __init__(self,max):
		self.curent_epoch = 0
		self.max_epoch = max

	def on_epoch_end(self,epoch,logs=None):
		self.curent_epoch = epoch
		if self.curent_epoch == 0:
			print("\n\n0 %")
		else:
			print("\n\n{} %".format(float(self.curent_epoch/self.max_epoch)))

