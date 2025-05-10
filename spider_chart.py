import matplotlib.pyplot as plt
import numpy as np
import csv

# Set font family globally to a sans-serif similar to 'Work Sans'
plt.rcParams['font.family'] = 'DejaVu Sans'  # or 'Arial', 'Liberation Sans', etc.

# Read CSV
filename = 'spider_data.csv'
series_names = []
data = []
thicknesses = []
dashstyles = []
colors = []
with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    output_mode_row = next(reader)
    output_mode = output_mode_row[1].strip().lower() if output_mode_row[0] == 'OutputMode' else 'show'
    title_row = next(reader)
    chart_title = title_row[1] if title_row[0] == 'Title' else 'Spider Chart'
    outer_circle_row = next(reader)
    outer_circle_thickness = int(outer_circle_row[1]) if outer_circle_row[0] == 'OuterCircleThickness' else 2
    spine_row = next(reader)
    spine_thickness = int(spine_row[1]) if spine_row[0] == 'SpineThickness' else 1
    header = next(reader)
    axis_labels = header[1:-3]  # Exclude 'Thickness', 'DashStyle', 'Color' columns
    axis_labels = [lbl.replace('\n', '\n').replace('\n', '\n') for lbl in axis_labels]
    tick_labels = next(reader)[1:-3]  # Custom tick labels
    for row in reader:
        series_names.append(row[0])
        data.append([float(x) for x in row[1:-3]])  # Exclude 'Thickness', 'DashStyle', 'Color' columns
        thicknesses.append(int(row[-3]))  # Thickness values
        dashstyles.append(row[-2].strip())  # Dash style values
        colors.append(row[-1].strip())  # Color values

num_vars = len(axis_labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # close the circle

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True), constrained_layout=True)
fig.patch.set_facecolor('#18162a')
ax.set_facecolor('#18162a')
ax.spines['polar'].set_color('#fff')
ax.spines['polar'].set_linewidth(outer_circle_thickness)
# Use a brighter purple for the spiderweb grid
web_color = '#a78bfa'
ax.grid(color=web_color, linewidth=spine_thickness, linestyle='dotted', alpha=0.7)

# Draw each series
for idx, values in enumerate(data):
    values = values + values[:1]  # close the circle
    ax.plot(angles, values, color=colors[idx], linewidth=thicknesses[idx], label=series_names[idx], linestyle=dashstyles[idx])

# Set the labels
ax.set_xticks(angles[:-1])
ax.set_xticklabels(axis_labels, color='#fff', fontsize=14, fontweight='bold')

# Move axis labels outward using labelpad, not manual position
ax.xaxis.set_tick_params(pad=20)

# Set the y-labels (radial ticks) along each spine
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(tick_labels[:5], color='#bdbdfc', fontsize=12)  # Use first 5 tick labels
ax.yaxis.grid(True, color=web_color, linestyle='dotted', alpha=0.5)
ax.tick_params(axis='y', labelsize=10)

# Optional: Title and legend
plt.title(chart_title, color='#fff', fontsize=22, fontweight='bold', pad=24)
legend = ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), frameon=False, fontsize=16)
for text in legend.get_texts():
    text.set_fontweight('bold')
    text.set_color('#fff')

# Show or save the chart based on OutputMode
if output_mode == 'save':
    plt.savefig('spider_chart.png', transparent=True, dpi=300)
else:
    plt.show() 