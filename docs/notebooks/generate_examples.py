from dummy_spatialdata import generate_dataset
import dummy_anndata
import spatialdata_plot as sdp 
import spatialdata as sd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import anndata as ad
import tempfile as tf
import shutil

# generate anndata
def generate_anndata(n_obs=12, n_vars=20):
    obs = pd.DataFrame(index=[f'obs_{i}' for i in range(n_obs)])
    var = pd.DataFrame(index=[f'var_{i}' for i in range(n_vars)])
    X = np.random.rand(n_obs, n_vars)
    adata = ad.AnnData(X=X, obs=obs, var=var)
    return adata

# generate spatialdata
sdata = generate_dataset(
    images = [
        {'type': 'rgb', 'scale_factors': [2,2,2], 'coordinate_system': ['identity', 'scale', 'mapAxis', 'translation', 'rotation', 'affine', 'sequence']},
    ],
    labels = [
        {'n': 12, 'scale_factors': [2,2,2], 'coordinate_system': ['identity', 'scale', 'mapAxis', 'translation', 'rotation', 'affine', 'sequence']},
    ],
    shapes = [
        {'n': 12, 'type': 'polygon', 'coordinate_system': ['identity', 'scale', 'mapAxis', 'translation', 'rotation', 'affine', 'sequence']},
        {'n': 12, 'type': 'circle', 'coordinate_system': ['identity', 'scale', 'mapAxis', 'translation', 'rotation', 'affine', 'sequence']}
    ],
    points = [
        {'n': 12, 'coordinate_system': ['identity', 'scale', 'mapAxis', 'translation', 'rotation', 'affine', 'sequence']} 
    ],
    tables = [
        {'table': generate_anndata(n_obs=12, n_vars=20), 'element': 'shape', 'element_index': 0},
        {'table': generate_anndata(n_obs=12, n_vars=20), 'element': 'shape', 'element_index': 1}
    ],
    coordinate_systems = {
        'identity': {'transformations': ['identity'], 'shape':{'x': 500, 'y': 500}},
        'scale': {'transformations': ['scale'], 'shape':{'x': 500, 'y': 500}},
        'mapAxis': {'transformations': ['mapAxis'], 'shape':{'x': 500, 'y': 500}},
        'translation': {'transformations': ['translation'], 'shape':{'x': 500, 'y': 500}},
        'rotation': {'transformations': ['rotation'], 'shape':{'x': 500, 'y': 500}},
        'affine': {'transformations': ['affine'], 'shape': {'x': 500, 'y': 500}},
        'sequence': {'transformations': ['scale', 'mapAxis', 'translation', 'rotation', 'affine'], 'shape':{'x': 500, 'y': 500}}
    },
    SEED=13
)

# write to temp
filename = tf.NamedTemporaryFile()
filename.name + ".zarr"
sdata.write(filename.name + ".zarr")

# read back
sdata = sd.read_zarr(filename.name + ".zarr")
print(sdata)

# zip 
folder_to_zip = filename.name + ".zarr"
output_zip = tf.NamedTemporaryFile()
output_zip = output_zip.name + "/data"
shutil.make_archive(output_zip, 'zip', folder_to_zip)
print(output_zip)