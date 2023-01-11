import pandas as pd

df_data = pd.read_csv("../../input/input_data.csv")

ignore_mutation = []

for index in df_data.index:
    if "*" in df_data["hgvs_pro"][index]:
        ignore_mutation.append(1)
    else:
        ignore_mutation.append(0)

df_data["ignore"] = ignore_mutation

filter_mutations = df_data.loc[df_data["ignore"] == 0]
filter_mutations = filter_mutations.reset_index()

wild_residues = []
position_list = []
mutant_residues = []

for index in filter_mutations.index:
    mutation_value = filter_mutations["hgvs_pro"][index][2:]
    wild_residue = mutation_value[:3]
    mut_residue = mutation_value[-3:]
    position = mutation_value[3:-3]

    wild_residues.append(wild_residue)
    mutant_residues.append(mut_residue)
    position_list.append(position)

filter_mutations["wild_residue"] = wild_residues
filter_mutations["positions"] = position_list
filter_mutations["mut_residue"] = mutant_residues

filter_mutations.to_csv("../../results/1_process_data.csv", index=False)
