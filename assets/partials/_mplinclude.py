import matplotlib.pyplot as plt
from cycler import cycler

plt.style.use("../../../assets/templates/publish.mplstyle")

carbon_colors = [
    ("#6929c4", "Purple 70"),
    ("#1192e8", "Cyan 50"),
    ("#005d5d", "Teal 70"),
    ("#9f1853", "Magenta 70"),
    ("#fa4d56", "Red 50"),
    ("#570408", "Red 90"),
    ("#198038", "Green 60"),
    ("#002d9c", "Blue 80"),
    ("#ee538b", "Magenta 50"),
    ("#b28600", "Yellow 50"),
    ("#009d9a", "Teal 50"),
    ("#012749", "Cyan 90"),
    ("#8a3800", "Orange 70"),
    ("#a56eff", "Purple 50"),
]
custom_colors = [color[0] for color in carbon_colors]

# Define a list of line styles
line_styles = [
    "-",  # solid
    "--",  # dashed
    "-.",  # dash-dot
    ":",  # dotted
    (0, (1, 10)),  # custom dash pattern 1
    (0, (5, 10)),  # custom dash pattern 2
    (0, (3, 10, 1, 10)),  # custom dash pattern 3
    (0, (5, 5)),  # custom dash pattern 4
    (0, (5, 1)),  # custom dash pattern 5
    (0, (3, 5, 1, 5)),  # custom dash pattern 6
    (0, (1, 1)),  # custom dash pattern 7
    (0, (3, 1, 1, 1)),  # custom dash pattern 8
    (0, (1, 5)),  # custom dash pattern 9
    (0, (5, 5, 1, 5)),  # custom dash pattern 10
]

# plt.rc('axes', prop_cycle=(plt.cycler('color', custom_colors)))
# plt.rc('axes', prop_cycle=(cycler('color', custom_colors) * cycler('linestyle', line_styles)))
combined_cycle = cycler(color=custom_colors) + cycler(linestyle=line_styles)
plt.rc("axes", prop_cycle=combined_cycle)
