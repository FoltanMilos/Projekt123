import keras.callbacks as ker_clbck

# trieda na zavolanie evaulate po jednej epoche
# robi v podstate validaciu, daju sa sem vsak podhodit data exante pre sledovanie
# zmeny generalizovania pocas behu ucenia
class Callbacks(ker_clbck.Callback):
	def __init__(self,test_data,test_lab,model):
		self.test_data = test_data
		self.test_labels = test_lab
		self.md = model

	def on_epoch_end(self,epoch,logs={}):
		#loss, acc = self.md.test_model(self.test_data,self.test_labels)
		loss, acc = self.model.evaluate(self.test_data, self.test_labels, verbose=0)
		print('\nTesting loss: {}, acc: {}\n'.format(loss, acc))

