import numpy as np

# Kernels

identity_kernel = np.array([
    0, 0, 0,
    0, 1, 0,
    0, 0, 0
])

sharpen_kernel = np.array([
    -1, -1, -1,
    -1,  9, -1,
    -1, -1, -1
])

blur_kernel = (1 / 16) * np.array([
    1, 2, 1,
    2, 4, 2,
    1, 2, 1,
])

edges_kernel = np.array([
    -1, -1, -1,
    -1,  8, -1,
    -1, -1, -1,
])

emboss_kernel = np.array([
    -2, -1, 0,
    -1,  1, 1,
     0,  1, 2
])
