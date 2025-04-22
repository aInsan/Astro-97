import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Data from the experiment
temperatures = ["10°C", "15°C", "22°C", "30°C"]
day7_heights = [1.2, 2.3, 3.7, 2.9]
day14_heights = [2.8, 4.5, 7.2, 5.6]

# Create DataFrame for easier plotting
data = {
    "Temperature": temperatures,
    "Day 7": day7_heights,
    "Day 14": day14_heights
}

# Set up the figure
plt.figure(figsize=(10, 6))

# Set width of bars
barWidth = 0.3

# Set positions of the bars on X axis
r1 = np.arange(len(temperatures))
r2 = [x + barWidth for x in r1]

# Create bars
plt.bar(r1, day7_heights, width=barWidth, edgecolor='grey', label='Day 7', color='skyblue')
plt.bar(r2, day14_heights, width=barWidth, edgecolor='grey', label='Day 14', color='royalblue')

# Add xticks on the middle of the group bars
plt.xlabel('Temperature', fontweight='bold', fontsize=12)
plt.ylabel('Plant Height (cm)', fontweight='bold', fontsize=12)
plt.xticks([r + barWidth/2 for r in range(len(temperatures))], temperatures)
plt.title('Plant Growth at Different Temperatures', fontsize=14, fontweight='bold')

# Add a grid for better readability
plt.grid(True, linestyle='--', alpha=0.7, axis='y')

# Create legend & show graphic
plt.legend()

# Add value labels on top of each bar
for i, v in enumerate(day7_heights):
    plt.text(i, v + 0.1, str(v), ha='center')

for i, v in enumerate(day14_heights):
    plt.text(i + barWidth, v + 0.1, str(v), ha='center')

# Optional: Add a note about the experiment
plt.figtext(0.5, 0.01, 'Garden Cress (Lepidium sativum) growth experiment over 14 days', 
            ha='center', fontsize=9, style='italic')

# Adjust layout and save
plt.tight_layout(pad=2.0)
plt.savefig('plant_growth_chart.png', dpi=300, bbox_inches='tight')
plt.show()