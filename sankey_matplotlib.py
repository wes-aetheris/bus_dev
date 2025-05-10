import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey

# Read the CSV data
csv_file = 'sankey_data.csv'
df = pd.read_csv(csv_file)

# Build node list and mapping
all_nodes = pd.unique(df[['Source', 'Target']].values.ravel('K'))
node_indices = {name: idx for idx, name in enumerate(all_nodes)}

# Build flows and labels for matplotlib Sankey
flows = []
labels = []
orientations = []

# Calculate net flow for each node
net_flow = {name: 0 for name in all_nodes}
for _, row in df.iterrows():
    net_flow[row['Source']] -= row['Value']
    net_flow[row['Target']] += row['Value']

# Add flows for each node, and append value to label
for name in all_nodes:
    flows.append(net_flow[name])
    labels.append(f"{name} ({net_flow[name]})")
    orientations.append(0)  # 0 = horizontal

# Create the Sankey diagram
fig, ax = plt.subplots(figsize=(10, 6))
sankey = Sankey(ax=ax, unit=None, scale=1.0, gap=0.5)
sankey.add(flows=flows, labels=labels, orientations=orientations)
sankey.finish()

plt.title('Sankey Diagram from CSV (Matplotlib)', fontsize=18, fontweight='bold')
plt.tight_layout()
plt.show() 