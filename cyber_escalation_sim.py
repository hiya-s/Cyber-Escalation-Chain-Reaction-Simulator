# cyber_escalation_sim.py

import simpy
import random
import matplotlib.pyplot as plt
import networkx as nx

# --- Define Systems and Their Dependencies ---
system_dependencies = {
    'Power Grid AI': [],
    'Internet Backbone AI': ['Power Grid AI'],
    'Smart Water Utility': ['Power Grid AI'],
    'Data Centers': ['Power Grid AI', 'Internet Backbone AI'],

    'Hospitals': ['Power Grid AI', 'Smart Water Utility', 'Internet Backbone AI'],
    'Finance': ['Internet Backbone AI', 'Power Grid AI'],
    'Logistics': ['Internet Backbone AI', 'Power Grid AI'],
    'Public Transit': ['Internet Backbone AI', 'Power Grid AI'],
    'Smart Manufacturing': ['Power Grid AI', 'Internet Backbone AI'],

    'Emergency Services': ['Power Grid AI', 'Internet Backbone AI'],
    'Media': ['Internet Backbone AI', 'Data Centers'],
    'Government Portals': ['Internet Backbone AI', 'Data Centers'],
    'Food Supply Chain': ['Logistics', 'Smart Water Utility', 'Power Grid AI']
}

# Store each system's failure info
systems = {}
for name in system_dependencies:
    systems[name] = {
        'failed': False,
        'failure_time': None,
        'depends_on': system_dependencies[name]
    }

# Probability and delay ranges
failure_prob = 0.85
delay_range = (3, 20)

# --- SimPy Failure Logic ---
def fail_system(env, system_name):
    if systems[system_name]['failed']:
        return

    systems[system_name]['failed'] = True
    systems[system_name]['failure_time'] = env.now

    for target, props in systems.items():
        if system_name in props['depends_on'] and not props['failed']:
            if random.random() < failure_prob:
                delay = random.randint(*delay_range)
                env.process(fail_after_delay(env, target, delay))

    yield env.timeout(0)  # Ensure this is a generator

def fail_after_delay(env, system_name, delay):
    yield env.timeout(delay)
    yield env.process(fail_system(env, system_name))

def run_simulation(initial_failures, until=300):
    global systems
    # Reset all systems
    for name in systems:
        systems[name]['failed'] = False
        systems[name]['failure_time'] = None

    env = simpy.Environment()

    def init_fail():
        yield env.timeout(1)
        for sys in initial_failures:
            yield env.process(fail_system(env, sys))

    env.process(init_fail())
    env.run(until=until)
    return {k: v['failure_time'] for k, v in systems.items() if v['failed']}

# --- Visualization ---
def plot_failures(failure_times):
    if not failure_times:
        print("No failures occurred.")
        return

    items = sorted(failure_times.items(), key=lambda x: x[1])
    names, times = zip(*items)

    plt.figure(figsize=(12, 6))
    plt.barh(names, times, color='crimson')
    plt.xlabel('Failure Time in minutes')
    plt.title('Failure Timeline from Initial Cyber Event')
    plt.gca().invert_yaxis()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

# --- Example Run ---
if __name__ == '__main__':
    failures = run_simulation(['Power Grid AI'], until=100)
    plot_failures(failures)
