'''
    input: [filename_obrazka | vstupny_vektor]
    result: [vysledok klasifikacie]
    metadata: [vek, pohlavie a podobne, label ak to je v train alebo test mnozine None pre predikciu]
    run_length: casova dlzka vypoctu
'''
class Result:
    def __init__(self, model_input, result, metadata, prediction_length):
        self.model_input, self.result, self.metadata, self.run_length = model_input, result, metadata, prediction_length
