import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your CSV
df = pd.read_csv('failure_data.csv')

# Pivot the data: rows=System, columns=Run, values=FailureTime
heatmap_data = df.pivot(index='System', columns='Run', values='FailureTime')

# Optional: Fill missing failure times with a large number or NaN for better visualization
heatmap_data = heatmap_data.fillna(999)  # or np.nan

# Plot heatmap
plt.figure(figsize=(15, 10))
sns.heatmap(
    heatmap_data,
    cmap='YlOrRd',
    linewidths=0.5,
    linecolor='gray',
    cbar_kws={'label': 'Failure Time (minutes)'},
    xticklabels=10,  # Show every 10th run label for clarity
    yticklabels=True
)
plt.title('Failure Times Heatmap Across Simulation Runs')
plt.xlabel('Simulation Run')
plt.ylabel('System')
plt.show()
