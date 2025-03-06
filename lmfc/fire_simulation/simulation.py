import numpy as np

def compute_lfmc(ndmi, avg_ndmi, T60, W7):
    """
    Compute the Live Fuel Moisture Content (LFMC) using NDMI and meteorological data.
    
    ndmi: Current NDMI value
    avg_ndmi: Average NDMI value over the site
    T60: Mean temperature over last 60 days
    W7: Mean wind speed over last 7 days
    """
    lfmc = 177.45 - 79.85 * avg_ndmi + 142.13 * ndmi - 2.50 * T60 - 4.08 * W7
    # Normalize LFMC within a reasonable expected range (30% - 200%)
    lfmc = np.clip(lfmc, 30, 200)  # Clip to avoid extreme values
    normalized_lfmc = (lfmc - 30) / (200 - 30)  # Normalize between 0 and 1
    return normalized_lfmc


def fire_spread_simulation(fuel_map, ndvi, num_ignition_points=1, steps=100, spread_prob=0.5, wind_factor=1.2):
    fire_grid = np.zeros_like(fuel_map)
    
    # Create a mask for areas where fire should NOT spread
    non_burnable_mask = (fuel_map < 0.22) | (ndvi < -0.05)
    
    # Set ignition points
    ignition_points = np.array([[596, 604]])  # Single ignition point for testing
    
    for point in ignition_points:
        fire_grid[tuple(point)] = 1  # Mark as burning
    
    fire_sequence = [fire_grid.copy()]
    
    # Define wind direction impact (favoring SW, reducing NE)
    wind_modifiers = {
        (-1, 0): 1 / (wind_factor + 0.14),  # North (harder to spread)
        (1, 0): wind_factor,               # South (easier to spread)
        (0, -1): wind_factor**2.5,         # West (easier to spread)
        (0, 1): 1 / (wind_factor + 0.2),   # East (harder to spread)
        (-1, -1): 1 / (wind_factor + 0.3), # NW (neutral)
        (1, -1): wind_factor**3.2,           # SW (most affected by wind)
        (-1, 1): 1 / (wind_factor + 0.4),  # NE (most reduced by wind)
        (1, 1): 1 / (wind_factor + 0.2)    # SE (neutral but slightly reduced)
    }
    
    for _ in range(steps):
        new_fire_grid = fire_grid.copy()
        for i in range(1, fuel_map.shape[0] - 1):
            for j in range(1, fuel_map.shape[1] - 1):
                if fire_grid[i, j] == 1:
                    new_fire_grid[i, j] = 2  # Mark as burned
                    for (x, y), wind_effect in wind_modifiers.items():
                        ni, nj = i + x, j + y
                        
                        # Skip non-burnable areas
                        if non_burnable_mask[ni, nj]:
                            continue  # Do not allow fire to spread here

                        if fire_grid[ni, nj] == 0:  # Not yet burned
                            lfmc_effect = np.exp(-fuel_map[ni, nj])  # Exponential decay for dry fuels
                            adjusted_prob = spread_prob * lfmc_effect * wind_effect
                            if np.random.rand() < adjusted_prob:
                                new_fire_grid[ni, nj] = 1  # Ignite new cell
        
        fire_grid = new_fire_grid.copy()
        fire_sequence.append(fire_grid.copy())
    
    return fire_sequence