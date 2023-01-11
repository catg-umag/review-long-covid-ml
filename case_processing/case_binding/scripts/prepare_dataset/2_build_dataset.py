import pandas as pd


def create_sequence(pos, wild, mut, sequence):

    response = ""
    if sequence[pos] == wild:
        response = []
        for i in range(len(sequence)):
            if i == pos:
                response.append(mut)
            else:
                response.append(sequence[i])
        response = "".join(map(str, response))
    else:
        response = "ERROR"

    return response


dict_residues = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "GLU": "E",
    "GLN": "Q",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
}

df_data = pd.read_csv("../../results/1_process_data.csv")
sequence = (
    "NITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDL"
    "CFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYN"
    "YLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRV"
    "VVLSFELLHAPATVCGPKKST"
)
sequence_as_list = [res for res in sequence]

sequence_list = []

for index in df_data.index:
    pos = df_data["positions"][index] - 1
    wild = dict_residues[df_data["wild_residue"][index].upper()]
    mut = dict_residues[df_data["mut_residue"][index].upper()]
    response = create_sequence(pos, wild, mut, sequence_as_list)

    sequence_list.append(response)

df_data["sequence"] = sequence_list

df_export = df_data[["sequence", "average"]]
df_export.to_csv("../../results/2_df_to_encode.csv", index=False)
