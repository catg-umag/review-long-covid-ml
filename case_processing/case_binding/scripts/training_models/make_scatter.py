import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import r2_score

path_input = "../../results/"
plot_data = ["Secondary structure", "Volume", "Hydrophobicity"]

groups = [4, 6, 7]

fig, axes = plt.subplots(1, 3, figsize=(12, 6))

for i in range(len(groups)):

    name_df = "{}Group_{}/predictions_to_plot.csv".format(path_input, groups[i])

    df_data = pd.read_csv(name_df)

    r2_score_value = r2_score(df_data["Real values"], df_data["Predictions"])

    g = sns.scatterplot(
        ax=axes[i], x="Real values", y="Predictions", palette="colorblind", data=df_data
    )

    text_data = "$R^2 = {}$".format(round(r2_score_value, 2))

    g.text(
        -1.1,
        -4.7,
        text_data,
        horizontalalignment="left",
        size="medium",
        color="black",
        weight="semibold",
    )

    axes[i].set_xlim(-5, 0.3)
    axes[i].set_ylim(-5, 0.3)

    lims = [max(0.3, 0.3), min(-5, -5)]
    g.plot(lims, lims, "-r")
    axes[i].set_title(plot_data[i])

name_export = "{}plot_demo.png".format(path_input)
plt.savefig(name_export, dpi=300)
