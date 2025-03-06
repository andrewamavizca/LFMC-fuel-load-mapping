import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fire_simulation.preprocessing import split_into_patches, get_image_features
from fire_simulation.simulation import fire_spread_simulation, compute_lfmc
from fire_simulation.visualization import animate_fire_spread



# Load the image from the data folder
date = '11_06_18'
image = np.load(f'data/{date}_new.npy')

# Split the image into patches of size 1000x1000
patches = split_into_patches(image, patch_size=1000)

# Run the simulation on the first patch
steps = 250
patch = get_image_features(patches[0])
lfmc = compute_lfmc(patch['ndmi'], np.average(patch['ndmi']), 19.75, 5.36448)
fire_sequence = fire_spread_simulation(lfmc, patch['ndvi'], num_ignition_points=1, steps=steps)

# Visualize
animate_fire_spread(patch['rgb'], lfmc, fire_sequence, steps=steps)