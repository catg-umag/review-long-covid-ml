import os
import sys

import pandas as pd
from fft_encoding import FFTEncoding
from physicochemical_properties import PhysicochemicalEncoder

groups = ["Group_{}".format(i) for i in range(8)]

input_sequences = pd.read_csv(sys.argv[1])
encoders = pd.read_csv(sys.argv[2])
encoders.index = encoders["residue"]

path_export = sys.argv[3]

column_with_seq = "sequence"
column_with_id = "average"

for group in groups:

    command = "mkdir -p {}{}".format(path_export, group)
    os.system(command)

    print("Processing group: ", group)
    encoding_instance = PhysicochemicalEncoder(
        input_sequences, group, encoders, column_with_seq, column_with_id
    )

    df_physicochemical_encoding = encoding_instance.encoding_dataset()

    name_export = "{}{}/property_encoder.csv".format(path_export, group)
    df_physicochemical_encoding.to_csv(name_export, index=False)

    fft_encoding_instance = FFTEncoding(
        df_physicochemical_encoding,
        len(df_physicochemical_encoding.columns) - 1,
        column_with_id,
    )

    df_fft_encoding = fft_encoding_instance.encoding_dataset()

    name_export = "{}{}/fft_property_encoder.csv".format(path_export, group)
    df_fft_encoding.to_csv(name_export, index=False)
