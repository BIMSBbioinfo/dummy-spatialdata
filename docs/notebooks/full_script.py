'''
dummy-spatialdata is compatible with both spatialdata == 0.5.0 (zarr v2) and 0.7.2 (zarr v3)

Thus please use 
1. conda create --name dummy_sd_env python==3.12 spatialdata==0.7.2
or 
2. conda create --name dummy_sd_env_05 python==3.12 spatialdata==0.5.0 setuptools==75.8.0
'''

from dummy_spatialdata import generate_dataset
import dummy_anndata
import spatialdata as sd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import anndata as ad
import tempfile as tf

# generate anndata
adata = dummy_anndata.generate_dataset(n_obs=12, n_vars=20)

# generate spatialdata
sdata = generate_dataset(
    images = [
        {'type': 'rgb', 'scale_factors': [2,2,2], 'coordinate_system': 'global'},
        {'type': 'grayscale', 'scale_factors': [], 'coordinate_system': 'global'},
    ],
    labels = [
        {'n_labels': 12, 'scale_factors': [2,2,2], 'coordinate_system': 'global2'},
        {'n_labels': 12, 'scale_factors': [], 'coordinate_system': 'global2'},
    ], 
    shapes = [
        {'n_shapes': 12, 'coordinate_system': 'global'},
        {'n_shapes': 20},
    ],
    points = [
        {'n_points': 12}
    ],
    tables = [
        {'table': adata, 'element': 'shape', 'element_index': 0}
    ],
    coordinate_systems = {
        'global': {'transformations': ['affine'], 'shape': {'x': 2000, 'y': 2000}},
        'global2': {'transformations': ['scale', 'translation'], 'shape':{'x': 500, 'y': 500}}
    },
    SEED=13
)
print(sdata)


# write to temp
filename = tf.NamedTemporaryFile()
filename.name + '.zarr'
sdata.write(filename.name + '.zarr')

# read back
sdata = sd.read_zarr(filename.name + '.zarr')
print(sdata)