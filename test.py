import numpy as np

# Given values
wavelength = 360e-9  # meters
slit_width = 0.38e-3  # meters
theta = 24  # degrees

# Compute beta
beta = (np.pi * slit_width / wavelength) * np.sin(np.radians(theta))
print(beta)
print(np.sin(beta))
# Compute relative intensity
I_Imax = (np.sin(beta) / beta) ** 2

print(I_Imax)