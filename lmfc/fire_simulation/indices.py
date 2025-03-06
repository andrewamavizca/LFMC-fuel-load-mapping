def compute_index(numerator, denominator, epsilon=1e-10):
    denominator[denominator == 0] = epsilon  # Avoid division by zero
    return numerator / denominator

def compute_ndvi(red_band, nir_band):
    return compute_index(nir_band - red_band, nir_band + red_band)

def compute_ndmi(nir_band, swir_band):
    return compute_index(nir_band - swir_band, nir_band + swir_band)

def compute_nbr(nir_band, swir_band):
    return compute_index(nir_band - swir_band, nir_band + swir_band)

def compute_cwc(nir_band, swir_band):
    return compute_index(nir_band, swir_band)