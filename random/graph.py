import matplotlib.pyplot as plt
import numpy as np

# Define the data
stats = {
    'Goals': 30,
    'Assists': 9,
    'Shots per game': 5.1,
    'Dribbles per game': 5.7,
    'Passes per game': 50.3,
    'Tackles per game': 0.7
}

# Convert the data to arrays
categories = list(stats.keys())
values = np.array(list(stats.values()))

# Calculate the angle for each category
angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)

# Complete the circle
values = np.concatenate((values,[values[0]]))
angles = np.concatenate((angles,[angles[0]]))

# Create the plot
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(angles, values, 'o-', linewidth=2)
ax.fill(angles, values, alpha=0.25)
ax.set_thetagrids(angles * 180/np.pi, categories)
ax.grid(True)

# Add a title
plt.title("Messi's Stats")

# Show the plot
plt.show()
