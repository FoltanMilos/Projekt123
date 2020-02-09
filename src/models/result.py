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
        ret_json["Classification result"] = str("{:2.2f}".format(self.result*100)) + " %"
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
    def __init__(self):
        #name,age_aprox,anatom_site_general,benign_malignant,x_0_1,diagnosis,diagnosis_confirm_type,melanocytic,sex
        self.name = ''
        self.age_aprox = ''
        self.anatom_site_general = '' # popis
        self.benign_malignant = ''
        self.x_0_1 = ''
        self.diagnosis = ''
        self.diagnosis_confirm_type = ''
        self.melanocytic = ''
        self.sex = ''

    def to_json(self):
        ret_val = {}
        ret_val["name"] = str(self.name)
        ret_val["age_aprox"] = None if self.age_aprox is None else int(self.age_aprox)
        ret_val["anatom_site_general"] = str(self.anatom_site_general)
        ret_val["benign_malignant"] = str(self.benign_malignant)
        ret_val["x_0_1"] = str(self.x_0_1)
        ret_val["benign_malignant"] = str(self.benign_malignant)
        ret_val["diagnosis"] = str(self.diagnosis)
        ret_val["diagnosis_confirm_type"] = str(self.diagnosis_confirm_type)
        ret_val["sex"] = str(self.sex)
        return ret_val

    @staticmethod
    def loadCsvWithDatasetInfo(path):
        import bintrees as bst
        tree = bst.AVLTree()
        with open(file=path) as file:
            lines = file.readlines()
        i = 0
        dtNode = Metadata()
        for line in lines:
            if i > 0:
                splitted = line.split(";")
                dtNode.name = None if splitted[0] is None else str(splitted[0])
                dtNode.age_aprox = None if (splitted[1] is None or splitted[1] == '') else int(splitted[1])
                dtNode.anatom_site_general = None if splitted[2] is None else str(splitted[2])
                dtNode.benign_malignant = None if str(splitted[3]) is None else str(splitted[3])
                dtNode.x_0_1 = None if splitted[4] is None else str(splitted[4])
                dtNode.diagnosis = None if splitted[5] is None else str(splitted[5])
                dtNode.diagnosis_confirm_type = None if splitted[6] is None else str(splitted[6])
                dtNode.melanocytic = None if splitted[7] is None else str(splitted[7])
                dtNode.sex = None if splitted[8] is None else str(splitted[8])
                tree.insert(dtNode.name,dtNode)
            i += 1
        return tree