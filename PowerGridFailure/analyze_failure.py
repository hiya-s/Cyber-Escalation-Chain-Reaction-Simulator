import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Number of simulation runs used to normalize failure rate
NUM_RUNS = 100

# Load data
df = pd.read_csv('failure_data.csv')

# Plot average failure time
avg_df = df.groupby('System')['FailureTime'].mean().sort_values()

plt.figure(figsize=(12, 6))
sns.barplot(x=avg_df.values, y=avg_df.index, color='darkred')
plt.xlabel('Average Failure Time (minutes)')
plt.title('Average Failure Time over 100 Simulations')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# Plot failure rate
failure_counts = df['System'].value_counts()
failure_rate = (failure_counts / NUM_RUNS).sort_values()

plt.figure(figsize=(12, 6))
sns.barplot(x=failure_rate.values, y=failure_rate.index, color='steelblue')
plt.xlabel('Failure Probability')
plt.title('Failure Probability by System (over 100 runs)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
