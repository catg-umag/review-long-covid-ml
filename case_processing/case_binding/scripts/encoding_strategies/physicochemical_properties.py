import pandas as pd
from constant_values import ConstantValues
from joblib import Parallel, delayed


class PhysicochemicalEncoder:
    def __init__(
        self,
        dataset,
        property_encoder,
        dataset_encoder,
        name_column_seq,
        name_column_id,
    ):

        self.dataset = dataset
        self.property_encoder = property_encoder
        self.dataset_encoder = dataset_encoder
        self.name_column_seq = name_column_seq
        self.name_column_id = name_column_id

        self.zero_padding = self.check_max_size()

        self.constant_instance = ConstantValues()

    def __check_residues(self, residue):
        return residue in self.constant_instance.possible_residues

    def __encoding_residue(self, residue):
        if self.__check_residues(residue):
            return self.dataset_encoder[self.property_encoder][residue]
        return False

    def check_max_size(self):
        size_list = [len(seq) for seq in self.dataset[self.name_column_seq]]
        return max(size_list)

    def __encoding_sequence(self, sequence, id_seq):

        sequence = sequence.upper()
        sequence_encoding = []

        for i in range(len(sequence)):
            residue = sequence[i]
            response_encoding = self.__encoding_residue(residue)
            if response_encoding is not False:
                sequence_encoding.append(response_encoding)

        # complete zero padding
        for k in range(len(sequence_encoding), self.zero_padding):
            sequence_encoding.append(0)

        sequence_encoding.insert(0, id_seq)
        return sequence_encoding

    def encoding_dataset(self):

        # print("Start encoding process")
        data_encoding = Parallel(n_jobs=6, require="sharedmem")(
            delayed(self.__encoding_sequence)(
                self.dataset[self.name_column_seq][i],
                self.dataset[self.name_column_id][i],
            )
            for i in range(len(self.dataset))
        )

        print("Processing results")
        matrix_data = []
        for element in data_encoding:
            matrix_data.append(element)

        print("Creating dataset")
        header = ["p_{}".format(i) for i in range(len(matrix_data[0]) - 1)]
        header.insert(0, self.name_column_id)
        print("Export dataset")
        df_data = pd.DataFrame(matrix_data, columns=header)

        return df_data
