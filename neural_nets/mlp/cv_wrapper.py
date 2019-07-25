from math import floor
from neural_nets.mlp.mlp import Mlp


class CrossValidation:
    @staticmethod
    def cross_validate_mlp(self, nfolds, inputs, labels, mlp: Mlp):
        input_folds, label_folds = self.__get_folds__(nfolds, inputs, labels)
        cv_result = []
        for i in range(len(input_folds)):
            mlp.reset_weights()
            for j in range(len(input_folds)):
                if j != i:
                    mlp.learn(input_folds[j], label_folds[j])
            output = mlp.test(input_folds[i])
            err = [output[k][0] - label_folds[i][k][0] for k in range(len(output))]
            cv_result.append((output, err))
        return cv_result

    @staticmethod
    def __get_folds__(self, nfolds, inputs, labels):
        return self.__split__(nfolds, inputs), self.__split__(nfolds, labels)

    @staticmethod
    def __split__(self, nfolds, data):
        if len(data) % nfolds != 0:
            folds = self.__make_folds__(floor(len(data)/nfolds), data)
            folds.append(data[-(len(data) % nfolds):])
        else:
            folds = self.__make_folds__(nfolds, data)
        return folds

    @staticmethod
    def __make_folds__(nfolds, data):
        foldsize = int(len(data)/nfolds)
        folds = [data[i*foldsize:(i+1)*foldsize] for i in range(nfolds)]
        return folds
