import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load US states map (GeoJSON or shapefile)
us_gdf = gpd.read_file('us_states.geojson').to_crs(epsg=3857)

# Load failure data (make sure it has a 'State' column)
df = pd.read_csv('failure_data_us.csv')
run = 1
run_data = df[df.Run == run]

# Sort failure events by time
timeline = run_data[['State', 'FailureTime']].sort_values('FailureTime').values

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.axis('off')

def animate(frame):
    ax.clear()
    ax.axis('off')
    us_gdf.plot(ax=ax, color='lightgray', edgecolor='black')

    current_time = frame
    ax.set_title(f"US AI-Induced Cascading Failures\nTime: {current_time} minutes", fontsize=18)

    # States failed by current time
    failed_states = set(state for state, t in timeline if t <= current_time)

    if failed_states:
        us_gdf[us_gdf['NAME'].isin(failed_states)].plot(ax=ax, color='red', alpha=0.5)

max_time = int(run_data['FailureTime'].max()) + 2
ani = FuncAnimation(fig, animate, frames=range(0, max_time, 2), interval=1000)

ani.save("us_failure_escalation.gif", writer='pillow')

plt.show()
