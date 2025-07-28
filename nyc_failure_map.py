import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load NYC borough GeoJSON
gdf = gpd.read_file("nyc_boroughs.geojson").to_crs(epsg=3857)

# Load simulation failure data (Run 1 used here)
df = pd.read_csv('failure_data.csv')
run = 1
run_data = df[df.Run == run]

# System to borough mapping (simplified)
system_borough = {
    "Power Grid AI": ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"],
    "Internet Backbone AI": ["Manhattan", "Queens", "Brooklyn"],
    "Smart Water Utility": ["Bronx", "Queens"],
    "Data Centers": ["Brooklyn", "Queens"],
    "Hospitals": ["Brooklyn", "Bronx", "Manhattan"],
    "Finance": ["Manhattan"],
    "Logistics": ["Queens", "Brooklyn"],
    "Public Transit": ["Manhattan", "Bronx"],
    "Smart Manufacturing": ["Queens", "Brooklyn"],
    "Emergency Services": ["Bronx", "Manhattan"],
    "Media": ["Manhattan"],
    "Government Portals": ["Brooklyn"],
    "Food Supply Chain": ["Queens", "Brooklyn"]
}

# Realistic coordinates (EPSG:3857 projected)
system_locations = {
    # Power Grid substations (multiple key ones)
    "Power Grid AI": [
        (-8238517, 4970350),  # Manhattan Substation
        (-8235000, 4950000),  # Brooklyn Substation
        (-8230000, 4960000),  # Queens Substation
        (-8241000, 4980000),  # Bronx Substation
        (-8237000, 4940000),  # Staten Island Substation
    ],
    "Internet Backbone AI": [
        (-8239000, 4970000),  # Manhattan Data Hub
        (-8232000, 4962000),  # Queens Network Hub
        (-8236000, 4953000),  # Brooklyn Network Hub
    ],
    "Smart Water Utility": [
        (-8241000, 4981000),  # Bronx Water Plant
        (-8231000, 4959000),  # Queens Water Plant
    ],
    "Data Centers": [
        (-8235000, 4951000),  # Brooklyn Data Center 1
        (-8230500, 4958000),  # Queens Data Center 2
    ],
    "Hospitals": [
        (-8238500, 4971000),  # Manhattan Hospital
        (-8240000, 4980500),  # Bronx Hospital
        (-8235500, 4952000),  # Brooklyn Hospital
    ],
    "Finance": [
        (-8238000, 4970000),  # Wall Street Finance Center
    ],
    "Logistics": [
        (-8231500, 4961500),  # Queens Logistics Hub
        (-8234000, 4952500),  # Brooklyn Logistics Hub
    ],
    "Public Transit": [
        (-8238300, 4970100),  # Manhattan Transit Control
        (-8240200, 4980300),  # Bronx Transit Control
    ],
    "Smart Manufacturing": [
        (-8232500, 4958000),  # Queens Manufacturing Plant
        (-8234800, 4953000),  # Brooklyn Manufacturing Plant
    ],
    "Emergency Services": [
        (-8240200, 4980200),  # Bronx Emergency HQ
        (-8238300, 4970200),  # Manhattan Emergency HQ
    ],
    "Media": [
        (-8238100, 4970400),  # Manhattan Media Center
    ],
    "Government Portals": [
        (-8235400, 4951500),  # Brooklyn Government Offices
    ],
    "Food Supply Chain": [
        (-8231600, 4961800),  # Queens Food Supply Hub
        (-8234200, 4952600),  # Brooklyn Food Supply Hub
    ],
}

# Color & marker by system for plotting
system_styles = {
    "Power Grid AI": ('blue', 's'),
    "Internet Backbone AI": ('purple', '^'),
    "Smart Water Utility": ('cyan', 'o'),
    "Data Centers": ('green', 'D'),
    "Hospitals": ('orange', 'v'),
    "Finance": ('brown', 'p'),
    "Logistics": ('yellow', '*'),
    "Public Transit": ('pink', 'X'),
    "Smart Manufacturing": ('magenta', '<'),
    "Emergency Services": ('red', '>'),
    "Media": ('black', 'h'),
    "Government Portals": ('gray', 'P'),
    "Food Supply Chain": ('lime', '8'),
}

fig, ax = plt.subplots(figsize=(12, 12))
ax.axis('off')

# Prepare timeline sorted by failure time
timeline = run_data[['System', 'FailureTime']].sort_values('FailureTime').values

def animate(frame):
    ax.clear()
    ax.axis('off')
    # Draw base map
    gdf.plot(ax=ax, color='lightgray', edgecolor='black')

    current_time = frame
    ax.set_title(f"NYC AI-Induced Failure Escalation\nTime: {current_time} minutes", fontsize=16)

    # Systems failed by current time
    failed_systems = [sys for sys, t in timeline if t <= current_time]

    # Show all system nodes lightly
    for sys, locs in system_locations.items():
        color, marker = system_styles.get(sys, ('gray', 'o'))
        xs, ys = zip(*locs)
        # Plot all nodes with low alpha
        ax.scatter(xs, ys, c=color, marker=marker, alpha=0.3, s=80, edgecolors='k', label=sys)

    # Highlight failed nodes with big red circle marker
    for sys in failed_systems:
        if sys in system_locations:
            locs = system_locations[sys]
            xs, ys = zip(*locs)
            # Plot big red circles on failed nodes
            ax.scatter(xs, ys, c='red', s=300, marker='o', alpha=0.8, edgecolors='k', linewidths=1.5)

    # Shade boroughs that contain any failed system
    failed_boroughs = set()
    for sys in failed_systems:
        boros = system_borough.get(sys, [])
        failed_boroughs.update(boros)

    if failed_boroughs:
        gdf[gdf['BoroName'].isin(failed_boroughs)].plot(ax=ax, color='red', alpha=0.3)

    # Legend: show one sample per system (only once)
    handles = []
    labels = []
    for sys, (color, marker) in system_styles.items():
        handles.append(plt.Line2D([0], [0], marker=marker, color='w', label=sys,
                                  markerfacecolor=color, markersize=10, markeredgecolor='k', alpha=1))
        labels.append(sys)
    ax.legend(handles, labels, loc='lower left', bbox_to_anchor=(1.0, 0.1), fontsize=9)

max_time = int(run_data['FailureTime'].max()) + 2
ani = FuncAnimation(fig, animate, frames=range(0, max_time, 2), interval=1000)

ani.save("nyc_failure_detailed.gif", writer='pillow')

plt.show()
