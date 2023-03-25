import csv
import numpy as np
import matplotlib.pyplot as plt

path_csv = "n<32>y<30deg>x<sweep>.csv"

rows = []
with open(path_csv) as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

header = rows.pop(0)

data = np.float_(np.array(rows).T)

fig, ax = plt.subplots()

ax.plot(data[0], data[1])

ax.set_xlabel(header[0])
ax.set_ylabel(header[1])

ax.set_xlabel("$θ_x$ [deg]", fontsize=35)
ax.set_ylabel("$G_r$ [dB]", fontsize=35)

ax.grid()

ax.tick_params(labelsize=28)

plt.tight_layout()
plt.savefig("n<32>y<30deg>x<sweep>.png")
