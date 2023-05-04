import matplotlib.pyplot as plt
import matplotlib.colors as mc
import numpy as np
import csv
import pandas as pd

# https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib
def adjust_lightness(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


path = 'feature_importance_xyz.csv'




fig = plt.figure()
ax = fig.add_subplot(projection='3d')

headers = pd.read_csv(path, nrows=0).columns.tolist()
print(headers)
df = pd.read_csv(path, sep=',')
df = df.reset_index()

df = df.nlargest(150, 'importance')

upper_threshold = df['importance'].quantile(.96)
mid_threshold = df['importance'].quantile(.85)

color = mc.cnames['green']

for row in df.itertuples():
    x = row.deceased_avg_expression
    y = row.survivors_avg_expression
    z = row.importance
    ax.scatter(x, y, z, color=adjust_lightness(color, z/.002))

    if z > upper_threshold:
        ax.text(x * (1 + 0.01), y * (1 + 0.01), z * (1 + 0.01), row.gene, fontsize=7)

#print(df.columns)

#n = 100

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].

#ax.scatter(df['deceased_avg_expression'], df['survivors_avg_expression'], df['importance'])

ax.set_zlabel('importance')
ax.set_xlabel('deceased avg expression')
ax.set_ylabel('survivors avg expression')

ax.set_xlim((0,1))
ax.set_ylim((0,1))

plt.title("Top 150 most important genes (random forest)")
plt.show()
