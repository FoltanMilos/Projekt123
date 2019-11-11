'''
    input: [filename_obrazka | vstupny_vektor]
    result: [vysledok klasifikacie]
    metadata: [vek, pohlavie a podobne, label ak to je v train alebo test mnozine None pre predikciu]
    run_length: casova dlzka vypoctu
'''
class Result:
    def __init__(self,result,result_class, meta,predict_info):
        #self.model_input = None ## netreba, na FE si uchovame fotku
        self.result = result              # cislo, napr 0.97
        if result_class == 1:
            self.result_class = "Bening"
        elif result_class == 0:
            self.result_class = "Malignant"
        else:
            self.result_class = "Wrong value"
        self.metadata = meta            # ak fotka je z datasetu, inac ked sa odfoti nemname desc
        self.prediction_info = predict_info     # nejake informacie o predikovanej hodnote, zatial to berme ako dummy
                                        # dake odporucanie

    def to_json(self):
        ret_json = {}
        ret_json["Classification result"] = str("{:2.2f}".format(self.result*100))
        ret_json["Classification class"] = str(self.result_class)
        ret_json["prediction_info"] = "Vysledna hodnota ukazuje na percentualnu moznost vyskytu rakoviny. Je to " \
                                      "informacna hodnota. Nase odporucanie: Ak je hodnota velmi vysoka, navstivte svojho" \
                                      " lekara a poradte sa snim o moznom vybere znamienka"
        if self.metadata is not None:
            ret_json["metadata"] = self.metadata.to_json()
        else:
            ret_json["metadata"] = None
        return ret_json

class Metadata:
    def __init__(self,gender,age,real_diag,diag_conf_type,diag_meta):
        self.gender = gender
        self.age = age
        self.real_diagnosis = real_diag
        self.diagnosis_confirm_type = diag_conf_type
        self.diagnosis_meta = diag_meta # ci je melanocytic

    def to_json(self):
        ret_val = {}
        ret_val["Gender"] = str(self.gender)
        ret_val["Age"] = str(self.age)
        ret_val["Real diagnosis"] = str(self.real_diagnosis)
        ret_val["Desc clinical diagnostis"] = str(self.diagnosis_confirm_type)
        ret_val["Melanocytic"] = str(self.diagnosis_meta)
        return ret_val