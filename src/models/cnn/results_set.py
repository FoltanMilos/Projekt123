import numpy as np
import config as conf

class Results_set:
	""" Trieda zodpoveda za procesing vystupov zo siete """

	global ref_model			# referencia na model
	global r_id					# result set id
	global is_changed			# ci sa nieco modifikovalo
	global is_new				# ci su novo vytvorene pre db

	global result_json
	global test_specificity
	global train_accuracy
	global test_sensitivity
	global train_result_path
	global test_result_path

	def __init__(self,ref_model,is_new):
		# referencia na model, aby sa vedelo, ktoremu modelu patri (1 model = 1 ResultSet)
		self.ref_model = ref_model
		self.is_changed = False
		self.is_new = is_new
		# NOVE
		self.result_json = None
		self.test_specificity= 0
		self.train_accuracy= 0
		self.test_accuracy = None
		self.test_sensitivity= 0

		self.train_result_path= None
		self.test_result_path= None
		self.false_positives = None
		self.true_negatives = None

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

	def process_result_matrix(self,predction_array,true_lab_array):
		if(predction_array.shape[0]!= true_lab_array.shape[0]):
			raise Exception("Result for matrix must be same shape. But shape is: prediction_array:{} true_lab_array{}".format(predction_array.shape,true_lab_array.shape))
		index = 0
		predction_array = np.argmax(predction_array,axis=1)
		#predction_array = predction_array.astype(int)
		for predicted_value in predction_array:
			self.result_matrix[predicted_value,int(true_lab_array[index])]+= 1
			self.samples_count = self.samples_count+1
			index = index + 1
		self.ref_model.ref_app.log.info(self.result_matrix)
		self.calc_accuracy()
		self.calc_sensitivity()
		self.calc_specificity()
		self.calc_positive_pred()
		self.cacl_negative_pred()

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
		self.test_sensitivity = float(self.result_matrix[1, 1]) / (self.result_matrix[1, 1] + self.result_matrix[0, 1])
		return self.test_sensitivity

	def calc_specificity(self):
		""" d / (c+d)"""
		if(self.samples_count <= 0):
			raise Exception("Samples count should be > 0, but it is {}".format(self.samples_count))
		self.test_specificity = float(self.result_matrix[0, 0]) / (self.result_matrix[0, 0] + self.result_matrix[1, 0])
		return self.test_specificity

	def calc_accuracy(self):
		""" Presnost modelu, vzorec a + d / (a+b+c+d)
			pre urcenie % je potrebne prenasobit 100"""
		if (self.samples_count <= 0):
			raise Exception("Samples count should be > 0, but it is {}".format(self.samples_count))
		self.test_accuracy = float(self.result_matrix[1,1] + self.result_matrix[0,0])/(self.samples_count)
		return self.test_accuracy

	def calc_positive_pred(self):
		""" Ked model predpovie bening, tak aka je pravdepodobnost ze aj tak bude"""
		if self.samples_count <= 0 or self.result_matrix[1, 1] + self.result_matrix[1, 0] == 0:
			self.false_positives = 0
		else:
			self.false_positives = self.result_matrix[1,1]/(self.result_matrix[1,1]+self.result_matrix[1,0])
		return self.false_positives

	def cacl_negative_pred(self):
		""" Model predpovie malig a aka je P ze aj bude malig"""
		if self.samples_count <= 0 or self.result_matrix[0, 0] + self.result_matrix[0, 1] == 0:
			self.true_negatives = 0
		else:
			self.true_negatives= self.result_matrix[0, 0] / (self.result_matrix[0, 0] + self.result_matrix[0, 1])
		return self.true_negatives


	# loading
	def load_state(self):
		ret_set_all = self.ref_model.ref_app.ref_db.select_statement("Select r.* from "+str(conf.database)+"_result r"
				" join "+str(conf.database)+"_MODEL m on(r.r_id=m.r_id) where m.m_id="+str(self.ref_model.m_id) +"")
		for ret_set in ret_set_all:
			self.r_id = ret_set[0]
			self.train_result_path = ret_set[1]
			self.test_sensitivity = ret_set[5]
			self.test_specificity = ret_set[6]
			self.train_accuracy = ret_set[7]
			if ret_set[2] == 'NULL':
				self.test_result_path = None
			else:
				self.test_result_path = ret_set[2]
			self.test_accuracy = None if ret_set[3]  is None else float(ret_set[3])
			if  ret_set[4] is not None:
				spl = ret_set[4].split(",")
				self.result_matrix[0,0] = int(spl[0])
				self.result_matrix[0, 1] = int(spl[1])
				self.result_matrix[1, 0] = int(spl[2])
				self.result_matrix[1, 1] = int(spl[3])
		self.samples_count = self.result_matrix[0,0] + self.result_matrix[0,1] +self.result_matrix[1,0] +self.result_matrix[1,1]
		self.is_new = False
		self.is_changed = False
		self.cacl_negative_pred()
		self.calc_positive_pred()

	def save_state(self):
		if self.is_changed and self.is_new == False :
			if self.test_result_path is None:
				res_path = "'NULL'"
			else:
				res_path = "'" + self.test_result_path + "'"
			test_sensi = 0 if self.test_sensitivity is None else str(self.test_sensitivity)
			test_speci = 0 if self.test_specificity is None else str(self.test_specificity)
			train_acc = 0 if self.train_accuracy is None else str(self.train_accuracy)
			test_acc = 0 if self.test_accuracy is None else str(self.test_accuracy)
			matrx = "'" + str(int(self.result_matrix[0,0])) +","+str(int(self.result_matrix[0,1])) +","+str(int(self.result_matrix[1,0])) +","+str(int(self.result_matrix[1,1])) +  "'"
			# update len
			self.ref_model.ref_app.ref_db.update_statement("update "+ str(conf.database) +"_result "
				"SET model_train_result_path='" + str(self.train_result_path) + "',"
				" train_accuracy=" + str(train_acc) + ","
				" test_matrix=" + str(matrx) + ","
				" model_test_result_path=" + res_path + ","
				" test_sensitivity=" + str(test_sensi) + ","
				" test_specificity=" +str(test_speci) + ","
				" test_accuracy=" + str(test_acc) +
				" where r_id=" + str(self.r_id) + "")
			self.ref_model.ref_app.ref_db.commit()
			return self.r_id
		elif self.is_new:
			# insert
			self.r_id = self.ref_model.ref_app.ref_db.insert_returning_identity("insert INTO "+str(conf.database)+"_result"
				"(MODEL_TRAIN_RESULT_PATH, test_sensitivity, test_specificity, train_accuracy, MODEL_TEST_RESULT_PATH) values "
				"(NULL,NULL,NULL,NULL,NULL)","r_id")
			self.ref_model.ref_app.ref_db.commit()
			return self.r_id

	def to_json(self):
		result_json = {}
		training = {}
		testing = {}
		training["Accuracy"] = str(self.train_accuracy)
		training["TrainingTime"] = str(0)

		testing["Accuracy"] = str(self.test_accuracy)
		testing["Specificity"] = str(self.test_specificity)
		testing["Senzitivity"] = str(self.test_sensitivity)
		testing["FalsePositives"] = str(self.false_positives)
		testing["TrueNegatives"] = str(self.true_negatives)

		# result dict
		result_json["testing"] = testing
		result_json["training"] = training
		return result_json