import plotly.graph_objects as go
import pandas as pd
import re
import csv

# Helper to convert hex color to rgba with alpha
def hex_to_rgba(hex_color, alpha=0.5):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f'rgba({r},{g},{b},{alpha})'
    return hex_color  # fallback for named colors

csv_file = 'sankey_data.csv'
output_mode = 'show'
label_mode = 'on'
diagram_label = 'Sankey Diagram from CSV'
header_row_idx = None
node_order_mode = 'off'

# Read metadata and find header row
with open(csv_file, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if line.startswith('OutputMode'):
            output_mode = line.strip().split(',')[1].lower()
        elif line.startswith('LabelMode'):
            label_mode = line.strip().split(',')[1].lower()
        elif line.startswith('DiagramLabel'):
            diagram_label = line.strip().split(',')[1]
        elif line.startswith('NodeOrderMode'):
            node_order_mode = line.strip().split(',')[1].lower()
        elif line.startswith('Source,Target,Value'):
            header_row_idx = idx
            break

if header_row_idx is None:
    raise ValueError("Could not find header row (Source,Target,Value,...) in CSV.")

df = pd.read_csv(csv_file, skiprows=header_row_idx)

# Create a list of all unique nodes
all_nodes = pd.unique(df[['Source', 'Target']].values.ravel('K'))
node_indices = {name: idx for idx, name in enumerate(all_nodes)}

# Calculate inflow, outflow, and net flow for each node
inflow = {name: 0 for name in all_nodes}
outflow = {name: 0 for name in all_nodes}
for _, row in df.iterrows():
    outflow[row['Source']] += row['Value']
    inflow[row['Target']] += row['Value']

# Identify the middle node (the one that is both a source and a target)
middle_nodes = set(df['Source']).intersection(set(df['Target']))

# Build node labels
node_labels = []
for name in all_nodes:
    if name in middle_nodes:
        node_labels.append(f"{name} (Total: {inflow[name]})")
    elif outflow[name] == 0:
        node_labels.append(f"{name} ({inflow[name]})")
    else:
        node_labels.append(f"{name} ({outflow[name]})")

if label_mode == 'off':
    node_labels = ['' for _ in node_labels]

# Assign node colors
node_colors = []
default_middle_color = "#a78bfa"
default_alpha = 0.5
for name in all_nodes:
    input_row = df[df['Source'] == name]
    output_row = df[df['Target'] == name]
    if name in middle_nodes:
        node_colors.append(hex_to_rgba(default_middle_color, default_alpha))
    elif not input_row.empty and pd.notna(input_row.iloc[0].get('InputColor', None)) and input_row.iloc[0]['InputColor']:
        alpha = float(input_row.iloc[0]['InputAlpha']) if pd.notna(input_row.iloc[0].get('InputAlpha', None)) and input_row.iloc[0]['InputAlpha'] != '' else default_alpha
        node_colors.append(hex_to_rgba(input_row.iloc[0]['InputColor'], alpha))
    elif not output_row.empty and pd.notna(output_row.iloc[0].get('OutputColor', None)) and output_row.iloc[0]['OutputColor']:
        alpha = float(output_row.iloc[0]['OutputAlpha']) if pd.notna(output_row.iloc[0].get('OutputAlpha', None)) and output_row.iloc[0]['OutputAlpha'] != '' else default_alpha
        node_colors.append(hex_to_rgba(output_row.iloc[0]['OutputColor'], alpha))
    else:
        node_colors.append(hex_to_rgba(default_middle_color, default_alpha))

# Assign link colors
link_colors = []
for _, row in df.iterrows():
    if pd.notna(row.get('InputColor', None)) and row['InputColor']:
        alpha = float(row['InputAlpha']) if pd.notna(row.get('InputAlpha', None)) and row['InputAlpha'] != '' else default_alpha
        link_colors.append(hex_to_rgba(row['InputColor'], alpha))
    elif pd.notna(row.get('OutputColor', None)) and row['OutputColor']:
        alpha = float(row['OutputAlpha']) if pd.notna(row.get('OutputAlpha', None)) and row['OutputAlpha'] != '' else default_alpha
        link_colors.append(hex_to_rgba(row['OutputColor'], alpha))
    else:
        link_colors.append(hex_to_rgba(default_middle_color, default_alpha))

# Build the Sankey diagram data
sources = df['Source'].map(node_indices)
targets = df['Target'].map(node_indices)
values = df['Value']

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=node_labels,
        color=node_colors
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=link_colors
    )
)])

fig.update_layout(
    title_text=diagram_label,
    width=1000,
    height=600,
    font_size=14,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

if output_mode == 'save':
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.write_image('sankey_diagram.png', format='png', scale=2, width=1000, height=600, engine='kaleido')
else:
    fig.show()

# if node_order_mode == 'on':
#     # Extract node order for input and output spaces
#     node_labels = fig['data'][0]['node']['label']
#     # Try to get y positions if available
#     node_ys = getattr(fig['data'][0]['node'], 'y', None)
#     if node_ys is not None:
#         order = sorted(zip(node_ys, node_labels))
#         print("Top-to-bottom node order:")
#         for y, label in order:
#             print(label)
#     else:
#         # If y is not available, print input and output node order by appearance
#         sources = df['Source']
#         targets = df['Target']
#         print("Input space node order (by first appearance as Source):")
#         seen = set()
#         for s in sources:
#             if s not in seen:
#                 print(s)
#                 seen.add(s)
#         print("Output space node order (by first appearance as Target):")
#         seen = set()
#         for t in targets:
#             if t not in seen:
#                 print(t)
#                 seen.add(t) 