import numpy as np
import src.config as conf


class Results_set:
	""" Trieda zodpoveda za procesing vystupov zo siete """

	global ref_model			# referencia na model
	global r_id					# result set id
	global is_changed			# ci sa nieco modifikovalo
	global is_new				# ci su novo vytvorene pre db

	global result_json
	global specificity
	global accuracy
	global senzitivity
	global train_result_path
	global test_result_path

	def __init__(self,ref_model,is_new):
		# referencia na model, aby sa vedelo, ktoremu modelu patri (1 model = 1 ResultSet)
		self.ref_model = ref_model
		self.is_changed = False
		self.is_new = is_new
		# NOVE
		self.result_json = None
		self.specificity= -1
		self.accuracy= -1
		self.senzitivity= -1
		self.train_result_path= None
		self.test_result_path= None
		self.test_accuracy = None

		# clasifikacny model bude mat maticu 2x2
		self.result_matrix = np.zeros(shape=(2,2))
		#  POLE JE NAOPAK !!!!!!!!!!!!!!!!!!!
		#			0      1
		#       0   d	   b
		#		1   c      a
		# VSETKO V PROGRAME STYM POCITA, SPECIFICITA JE NA INDEXE 1,1 !!!!!!!
		#--------------------------------------------------------#
		#					[True label]	 					 #
		#        NotPressented(Malignant-0)  Pressented(Bening-1)#
		# Positive(0)		a                    c               #
		# Negative(1)		b	                 d               #
		# [predicted]                                            #
		#--------------------------------------------------------#

		# pocet vzoriek
		self.samples_count = 0
		self.result_json = {}
		self.result_json["Accuracy"] = 0
		self.result_json["Specificity"] = 0
		self.result_json["Senzitivity"] = 0
		self.result_json["FalsePositives"] = 0
		self.result_json["TrueNegatives"] = 0
		self.result_json["TrainingTime"] = 0
		self.result_json["Epochs"] = 0
		self.result_json["Optimizer"] = 0
		self.result_json["LearningRate"] = 0

	def process_result_matrix(self,predction_array,true_lab_array,threshold):
		if(predction_array.shape[0]!= true_lab_array.shape[0]):
			raise Exception("Result for matrix must be same shape. But shape is: prediction_array:{} true_lab_array{}".format(predction_array.shape,true_lab_array.shape))
		index = 0
		predction_array = predction_array > threshold
		predction_array = predction_array.astype(int)
		for predicted_value in predction_array:
			self.result_matrix[predicted_value,int(true_lab_array[index])]+= 1
			self.samples_count = self.samples_count+1
			index = index + 1
		print(self.result_matrix)

	#def process_results(self,prediction_array,true_lab_array,true_lab_names):
	#	""" Spracovanie vysledkov generovanych cez predict_generator
	#		prediction_array --->  obsahuje pole predpovedi
	#		true_lab_array  ---> obsahuje pole vzorovych labelov"""
	#	prediction_array_01 = prediction_array > conf.threshold
	#	prediction_array_01 = prediction_array_01.astype(int)
	##	# proces string
	#	result_string = ''
	#	i = 0
	#	for k in prediction_array:
	##					   "  --> Diagnosis: {} --- Percentage: {:04.2f}%".format(true_lab_names[i], prediction_array_01[i],k[0]*100)
	#		i=i+1
	#
	#		# vysledky
	#		result_string+="\n\nTable:\n------[TRUE LABELS]-------\n" \
	#				   "---Malig(0)---Bening(1)---\n" \
	#				   "[0]   {0}      {1}     ---\n" \
	#				   "[1]   {2}      {3}     ---\n" \
	#				   "--------------------------".format(self.result_matrix[0,0],self.result_matrix[0,1],self.result_matrix[1,0],self.result_matrix[1,1])
	#	result_string+="\nSpecificity: {}".format(self.calc_specificity())
	#	result_string += "\nSensitivity: {}".format(self.calc_sensitivity())
	#	result_string += "\nAccuracy: {:04.2f}%".format(self.calc_accuracy()*100)
	#	print(result_string)
	#	return result_string

	# --------------[STATISTICS]----------------------
	def calc_sensitivity(self):
		""" Spocita sensitivitu z matrix tabulky, vzorec: [a/(a+b)"""
		if(self.samples_count <= 0):
			raise Exception("Samples count should be > 0, but it is {}".format(self.samples_count))
		self.senzitivity = float(self.result_matrix[1,1])/(self.result_matrix[1,1]+self.result_matrix[0,1])
		return self.senzitivity

	def calc_specificity(self):
		""" d / (c+d)"""
		if(self.samples_count <= 0):
			raise Exception("Samples count should be > 0, but it is {}".format(self.samples_count))
		self.specificity = float(self.result_matrix[0,0])/(self.result_matrix[0,0]+self.result_matrix[1,0])
		return self.specificity

	def calc_accuracy(self):
		""" Presnost modelu, vzorec a + d / (a+b+c+d)
			pre urcenie % je potrebne prenasobit 100"""
		if (self.samples_count <= 0):
			raise Exception("Samples count should be > 0, but it is {}".format(self.samples_count))
		self.test_accuracy = float(self.result_matrix[1,1] + self.result_matrix[0,0])/(self.samples_count)
		return self.test_accuracy

	def calc_positive_pred(self):
		""" Ked model predpovie bening, tak aka je pravdepodobnost ze aj tak bude"""
		if (self.samples_count <= 0):
			raise Exception("Samples count should be > 0, but it is {}".format(self.samples_count))
		return self.result_matrix[1,1]/(self.result_matrix[1,1]+self.result_matrix[1,0])

	def cacl_negative_pred(self):
		""" Model predpovie malig a aka je P ze aj bude malig"""
		if (self.samples_count <= 0):
			raise Exception("Samples count should be > 0, but it is {}".format(self.samples_count))
		return self.result_matrix[0,0]/(self.result_matrix[0,0]+self.result_matrix[0,1])


	# loading
	def load_state(self):
		ret_set_all = self.ref_model.ref_app.ref_db.select_statement("Select r.* from proj_result r"
				" join PROJ_MODEL m on(r.r_id=m.r_id) where m.m_id="+str(self.ref_model.m_id) +"")
		for ret_set in ret_set_all:
			self.r_id=ret_set[0]
			self.train_result_path = ret_set[1]
			self.senzitivity = ret_set[2]
			self.specificity = ret_set[3]
			self.accuracy = ret_set[4]
			self.test_result_path = ret_set[5]
			if  ret_set[9] is not None:
				spl = ret_set[9].split(",")
				self.result_matrix[0,0] = int(spl[0])
				self.result_matrix[0, 1] = int(spl[1])
				self.result_matrix[1, 0] = int(spl[2])
				self.result_matrix[1, 1] = int(spl[3])
		self.is_new = False
		self.is_changed = False


	def save_state(self):
		if self.is_changed and self.is_new == False :
			if self.test_result_path is None:
				res_path = "'NULL'"
			else:
				res_path = "'" + self.test_result_path + "'"
			sezi = -1 if self.senzitivity is None else str(self.senzitivity)
			speci = -1 if self.specificity is None else str(self.specificity)
			acc = -1 if self.accuracy is None else str(self.accuracy)
			matrx = "'" + str(int(self.result_matrix[0,0])) +","+str(int(self.result_matrix[0,1])) +","+str(int(self.result_matrix[1,0])) +","+str(int(self.result_matrix[1,1])) +  "'"
			# update len
			self.ref_model.ref_app.ref_db.update_statement("update proj_result "
				"SET model_train_result_path='" + str(self.train_result_path) + "',"
				" sensitivity=" + str(sezi) + ","
				" specificity=" + str(speci) + ","
				" accuracy=" + str(acc) + ","
				" test_matrix=" + str(matrx) + ","
				" model_test_result_path=" + res_path + " where r_id=" + str(self.r_id) + "")
			self.ref_model.ref_app.ref_db.commit()
			return self.r_id
		elif self.is_new:
			# insert
			self.r_id = self.ref_model.ref_app.ref_db.insert_returning_identity("insert INTO proj_result"
				"(MODEL_TRAIN_RESULT_PATH, SENSITIVITY, SPECIFICITY, ACCURACY, MODEL_TEST_RESULT_PATH) values "
				"(NULL,NULL,NULL,NULL,NULL)","r_id")
			self.ref_model.ref_app.ref_db.commit()
			return self.r_id

	def to_json(self):
		return self.result_json