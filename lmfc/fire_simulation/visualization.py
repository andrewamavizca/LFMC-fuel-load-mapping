import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib 
matplotlib.use('TkAgg') 
import matplotlib.colors as mcolors

# Define the colors based on the provided reference image
colors = [
    (0.3, 0.15, 0.0),  # Dark Brown
    (0.6, 0.4, 0.0),   # Lighter Brown
    (0.8, 0.6, 0.2),   # Yellow-Green
    (0.0, 0.5, 0.0),   # Green
    (0.0, 0.3, 0.0),   # Darker Green
    (0.0, 0.1, 0.0),   # Almost Black Green
    (0.0, 0.0, 0.0)    # Black
]


# Define the color mapping for fire spread simulation
fire_colors = {
    # Transparent
    #white
    0: (0,0,0,0),  # White (Unburned vegetation)
    # 0: "#000000",  # White (Unburned vegetation)
    # 0: "#228B22",  # Green (Unburned vegetation)
    1: "#FFD700",  # Bright Yellow-Gold (Actively Burning Fire)
    2: (1,1,1,0)   # Black (Burned out area)
}

# Create the colormap and corresponding bounds
fire_cmap = mcolors.ListedColormap([fire_colors[i] for i in sorted(fire_colors.keys())])
fire_norm = mcolors.BoundaryNorm(list(fire_colors.keys()) + [3], fire_cmap.N)
# Create colormap
custom_cmap = mcolors.LinearSegmentedColormap.from_list("custom_fuel_moisture", colors, N=256)


def animate_fire_spread(rgb_image, FLI, fire_sequence, steps=100):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=150)



    ax.imshow(FLI,cmap='hot_r', alpha=0.5, vmin=0, vmax=1)
    fire_im = ax.imshow(fire_sequence[0], cmap='hot', vmin=0, vmax=2, alpha=0.6)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    # ax[0].set_title('Fire Spread Simulation')
    

    def update(frame):
        fire_im.set_array(fire_sequence[frame])
        ax.set_title(f'Fire Spread Step {frame}')
        return [fire_im]
    global anim
    anim = animation.FuncAnimation(fig, update, frames=steps, interval=50, blit=False)
    # anim.save('fire_spread_simulation7.gif', writer='imagemagick', fps=60)
    plt.show()