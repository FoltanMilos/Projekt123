import neural_nets.cnn.model_cnn as cnn
import neural_nets.mlp.model_mlp as mlp
import neural_nets.genetic_alg.model_gen_alg as gen
import nn_type as n_type

class User:
	global u_id         #user id

	global models       #modely

	global ref_db       #connect na DB

	global active_model #aktivny model predikcii

	global ref_app      #na apku odkaz

	def __init__(self,ref_app,user_id,ref_db):
		self.models = []
		self.u_id = user_id
		self.ref_app = ref_app
		self.ref_db = ref_db

	def load_user_data(self):
		ret_models = self.ref_db.select_statement("select * from proj_model "
												 "where u_id ="+str(self.u_id)+" ")
		for loaded_model in ret_models:
			if(loaded_model[4] == n_type.Nn_type.CNN.value): #TODO: na CNN
				mod = cnn.Model_cnn(self.ref_app)
				mod.load_state(loaded_model)
				self.models.append(mod)
			elif():
				pass

	def save_user_data(self):
		# modely
		print("saving from user")
		for md in self.models:
			md.save_state()




	def register_model(self,model):
		self.models.append(model)