import src.models.cnn.model_cnn as cnn
import src.models.mlp.model_mlp as mlp
from src.enum import enum_model as n_type


class User:
	global u_id         # user id

	global models       # modely

	global ref_db       # connect na DB

	global active_model # aktivny model predikcii

	global ref_app      # na apku odkaz

	global is_changed   # ak sa nieco zmenilo, bude treba UPDATE, inac sa nic nerobi

	# from db
	global name			# meno usera

	global access		# pristup usera

	global indentifier 	# frontend identifier


	def __init__(self,ref_app,user_id,ref_db,identifier):
		self.models = []
		self.u_id = user_id
		self.ref_app = ref_app
		self.ref_db = ref_db
		self.is_changed = False
		self.indentifier = identifier

	def load_user_data(self):
		ret_models = self.ref_db.select_statement("select * from proj_model "
												 "where u_id ="+str(self.u_id)+"")
		for loaded_model in ret_models:
			if(loaded_model[4] == n_type.Nn_type.CNN.value):
				mod = cnn.Model_cnn(self,self.ref_app)
				mod.load_state(loaded_model)
				if(loaded_model[3] is not None):
					self.active_model = mod
				self.models.append(mod)
			elif(loaded_model[4] == n_type.Nn_type.MLP.value):
				mod = mlp.Model_mlp()
				mod.load_state(loaded_model)
				self.models.append(mod)
			elif():
				pass

	def save_user_data(self):
		if(self.is_changed==False):
			#nemusime nic ukladat v USEROVI
			pass
		else:
			self.ref_db.update_statement("update proj_user  .......")

		# CASCADE SAVING - treba vsetko pozriet, ci nie je zmena
		for md in self.models:
			md.save_state()

		# commit
		self.ref_db.commit()


	def register_model(self,model):
		self.models.append(model)

	def switch_active_model(self,new_act_model_id):
		for md in self.models:
			if(md.m_id == new_act_model_id):
				# prehodenie v DB
				self.ref_db.update_statement("update proj_model set m_active=null where m_id="+self.active_model.m_id)
				self.ref_db.update_statement("update proj_model set m_active='A' where m_id="+md._m_id)
				self.active_model = md
				return

	@staticmethod
	def load_all_users_no_cascade(app,db):
		ret_users = db.select_statement("select * from proj_user")
		list_users = []
		for loaded_user in ret_users:
			u = User(app, loaded_user[0], db)
			u.name = loaded_user[1]
			u.access = loaded_user[5]
			list_users.append(u)
		return list_users



