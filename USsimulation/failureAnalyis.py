import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load US states GeoJSON
gdf = gpd.read_file("us_states.geojson").to_crs(epsg=3857)

# Load failure simulation data (Run 1 used)
df = pd.read_csv('failure_data_us.csv')
run = 1
run_data = df[df.Run == run]

# System to states mapping (example)
system_states = {
    "Power Grid AI": ["California", "Texas", "New York", "Florida", "Illinois"],
    "Internet Backbone AI": ["New York", "Illinois", "Texas", "Washington"],
    "Smart Water Utility": ["California", "Arizona", "Nevada"],
    "Data Centers": ["Virginia", "Texas", "California"],
    "Hospitals": ["New York", "Florida", "Pennsylvania"],
    "Finance": ["New York", "Illinois"],
    "Logistics": ["Texas", "Georgia", "California"],
    "Public Transit": ["New York", "Illinois"],
    "Smart Manufacturing": ["Michigan", "Ohio", "Texas"],
    "Emergency Services": ["Florida", "Texas", "New York"],
    "Media": ["California", "New York"],
    "Government Portals": ["Virginia", "Washington DC"],
    "Food Supply Chain": ["California", "Iowa", "Illinois"]
}

fig, ax = plt.subplots(figsize=(25, 22))
ax.axis('off')

# Prepare sorted timeline of failures: (System, FailureTime)
timeline = run_data[['System', 'FailureTime']].sort_values('FailureTime').values

def animate(frame):
    ax.clear()
    ax.axis('off')
    # Plot base map
    gdf.plot(ax=ax, color='lightgray', edgecolor='black')

    current_time = frame
    ax.set_title(f"US AI-Induced Infrastructure Failures\nTime: {current_time} minutes", fontsize=18)

    # Determine failed systems by current frame
    failed_systems = [sys for sys, t in timeline if t <= current_time]

    # Collect all states that have any failed system
    failed_states = set()
    for sys in failed_systems:
        failed_states.update(system_states.get(sys, []))

    # Shade failed states in red with transparency
    if failed_states:
        gdf[gdf['NAME'].isin(failed_states)].plot(ax=ax, color='red', alpha=0.4)

# Animation frames from min to max failure time + buffer
min_time = int(run_data['FailureTime'].min())
max_time = int(run_data['FailureTime'].max()) + 5

ani = FuncAnimation(fig, animate, frames=range(min_time, max_time), interval=700)

ani.save("us_failure_regions.gif", writer='pillow')

plt.show()
