# monte_carlo_runner.py

import csv
from collections import defaultdict
from cyber_escalation_sim import run_simulation

NUM_RUNS = 100
initial_failures = ['Power Grid AI']
simulation_time = 300

# Store failure times for each system across runs
failure_times = defaultdict(list)

for i in range(NUM_RUNS):
    result = run_simulation(initial_failures, until=simulation_time)
    for system, fail_time in result.items():
        failure_times[system].append(fail_time)

# Save to CSV
with open('failure_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['System', 'Run', 'FailureTime'])
    for system, times in failure_times.items():
        for i, time in enumerate(times):
            writer.writerow([system, i+1, time])

print("Simulation complete. Data saved to failure_data.csv.")
