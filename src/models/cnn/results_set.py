import numpy as np
from src import config as conf


class Results_set:
	""" Trieda zodpoveda za procesing vystupov zo siete """

	global ref_model			# referencia na model

	global r_id					# result set id

	global is_changed			# ci sa nieco modifikovalo

	global is_new				# ci su novo vytvorene pre db

	def __init__(self,ref_model,is_new):
		# referencia na model, aby sa vedelo, ktoremu modelu patri (1 model = 1 ResultSet)
		self.ref_model = ref_model
		self.is_changed = False
		self.is_new = is_new

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
		# kontrola shapes
		if(predction_array.shape[0]!= true_lab_array.shape[0] or predction_array.shape[1] != true_lab_array.shape[1]):
			raise Exception("Result for matrix must be same shape. But shape is: prediction_array:{} true_lab_array{}".format(predction_array.shape,true_lab_array.shape))

		index = 0
		for predicted_value in predction_array:
			self.result_matrix[predicted_value,true_lab_array[index]]=self.result_matrix[predicted_value,true_lab_array[index]]+1
			self.samples_count = self.samples_count+1
			index = index + 1

	def process_results(self,prediction_array,true_lab_array,true_lab_names):
		""" Spracovanie vysledkov generovanych cez predict_generator
			prediction_array --->  obsahuje pole predpovedi
			true_lab_array  ---> obsahuje pole vzorovych labelov"""
		prediction_array_01 = prediction_array > conf.threshold
		prediction_array_01 = prediction_array_01.astype(int)
		self.process_result_matrix(predction_array=prediction_array_01,true_lab_array=true_lab_array)

		#print(classification_report(single_predict_img.classes, res, target_names=target_names))
		# proces string
		result_string = ''
		i = 0
		for k in prediction_array:
			result_string+="\nPhoto name: {:>28} " \
						   "  --> Diagnosis: {} --- Percentage: {:04.2f}%".format(true_lab_names[i], prediction_array_01[i],k[0]*100)
			i=i+1

		# vysledky
		result_string+="\n\nTable:\n------[TRUE LABELS]-------\n" \
					   "---Malig(0)---Bening(1)---\n" \
					   "[0]   {0}      {1}     ---\n" \
					   "[1]   {2}      {3}     ---\n" \
					   "--------------------------".format(self.result_matrix[0,0],self.result_matrix[0,1],self.result_matrix[1,0],self.result_matrix[1,1])
		result_string+="\nSpecificity: {}".format(self.calc_specificity())
		result_string += "\nSensitivity: {}".format(self.calc_sensitivity())
		result_string += "\nAccuracy: {:04.2f}%".format(self.calc_accuracy()*100)
		print(result_string)
		return result_string


	def process_single_result(self,single_result):
		""" Spracuje samostatnu predikciu, nepozera sa na TRUE label,je to viac menej to, ze nievieme urcit diagnosis"""
		percentage = 0
		pass

	# --------------[STATISTICS]----------------------
	def calc_sensitivity(self):
		""" Spocita sensitivitu z matrix tabulky, vzorec: [a/(a+b)"""
		if(self.samples_count <= 0):
			raise Exception("Samples count should be > 0, but it is {}".format(self.samples_count))
		return self.result_matrix[1,1]/(self.result_matrix[1,1]+self.result_matrix[0,1])

	def calc_specificity(self):
		""" d / (c+d)"""
		if(self.samples_count <= 0):
			raise Exception("Samples count should be > 0, but it is {}".format(self.samples_count))
		return self.result_matrix[0,0]/(self.result_matrix[0,0]+self.result_matrix[1,0])

	def calc_accuracy(self):
		""" Presnost modelu, vzorec a + d / (a+b+c+d)
			pre urcenie % je potrebne prenasobit 100"""
		if (self.samples_count <= 0):
			raise Exception("Samples count should be > 0, but it is {}".format(self.samples_count))
		return (self.result_matrix[1,1] + self.result_matrix[0,0])/(self.samples_count)

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
		ret_set_all = self.ref_model.ref_app.ref_db.select_statement("Select R_ID, R_MATRIX_A, R_MATRIX_B, R_MATRIX_C, R_MATRIX_D, R_SAMPLES_COUNT from proj_result"
				" join PROJ_MODEL using(r_id) where m_id="+str(self.ref_model.m_id) +"")
		if(len(ret_set_all) > 1 ):
			print("MODEL BY MAL MAT LEN JEDEN RESULT SET")
		for ret_set in ret_set_all:
			self.r_id=ret_set[0]
			self.samples_count = ret_set[5]
			self.result_matrix = np.zeros(shape=(2,2))
			self.result_matrix[0,0] = ret_set[4]
			self.result_matrix[1, 0] = ret_set[3]
			self.result_matrix[0, 1] = ret_set[2]
			self.result_matrix[1, 1] = ret_set[1]
			print(self.result_matrix)

	def save_state(self):
		if self.is_changed :
			# update len
			self.ref_model.ref_app.ref_db.update_statement("update proj_result "
				"SET R_MATRIX_A=" + str(self.result_matrix[1, 1]) + ","
				" R_MATRIX_B=" + str(self.result_matrix[0, 1]) + ","
				" R_MATRIX_C=" + str(self.result_matrix[1, 0]) + ","
				" R_MATRIX_D=" + str(self.result_matrix[0, 0]) + ","
				" R_SAMPLES_COUNT=" + str(self.samples_count) + " where r_id=" + str(self.r_id) + "")
			self.ref_model.ref_app.ref_db.commit()
			return self.r_id
		elif self.is_new:
			# insert
			self.r_id = self.ref_model.ref_app.ref_db.insert_returning_identity("insert INTO proj_result"
				"(R_MATRIX_A, R_MATRIX_B, R_MATRIX_C, R_MATRIX_D, R_SAMPLES_COUNT) values "
																				   #values(:1,:2,:3,:4,:5,:41)
				#(self.r_id,self.result_matrix[1, 1],self.result_matrix[0, 1],self.result_matrix[1, 0],self.result_matrix[0,0],self.samples_count))
				"("+str(self.result_matrix[1, 1])+","+str(self.result_matrix[0, 1])+","
				+ str(self.result_matrix[1, 0])+","+str(self.result_matrix[0,0])+","+str(self.samples_count)+")","r_id")
			self.ref_model.ref_app.ref_db.commit()
			return self.r_id