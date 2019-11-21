import keras.callbacks as ker_clbck


class LiveLearningCallback(ker_clbck.Callback):
	def __init__(self,max,modelId):
		self.curent_epoch = 0
		self.max_epoch = max
		self.modelId = modelId

	def on_epoch_end(self,epoch,logs=None,):
		self.curent_epoch = epoch
		resp = {'epoch': self.curent_epoch, 'max_epoch': self.max_epoch}
		tmp = {}
		for item in logs:
			tmp[item] = str(float(logs[item]))
		resp['data']= tmp
		if self.curent_epoch == 0:
			print("\n\n0 %")
			if self.callback is not None:
				self.callback('live-' + str(self.modelId), resp)
		else:
			print("\n\n{} %".format(float(self.curent_epoch/self.max_epoch)))
			if self.callback is not None:
				self.callback('live-' + str(self.modelId), resp)

	def on_train_end(self,logs=None,):
		if self.callback is not None:
			self.callback('live-' + str(self.modelId) + '-end', '')


	def setResponseFunc(self, callback):
		self.callback = callback