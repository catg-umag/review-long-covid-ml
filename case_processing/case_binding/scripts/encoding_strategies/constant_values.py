RESIDUES = list("ACDEFGHINKLMPQRSTVWY")


class ConstantValues:
    def __init__(self):
        self.n_cores = 4
        self.possible_residues = RESIDUES

        self.dict_value = {res: i for i, res in enumerate(sorted(RESIDUES))}
