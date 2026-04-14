import os
import sys
import numpy as np

from pathlib import Path
from importlib.resources import files, as_file
from PIL import Image
from typing import Optional
from spatialdata.models import TableModel
import spatialdata as sd
from .utils import default_shape

import anndata as ad
import pandas as pd

def generate_tablemodel(
    input: Optional[dict] = None
) -> TableModel:
    """Generate a dummy TableModel object with specified elements.

    Parameters
    ----------
    table: dict
        A dictionary of key value pairs with 
            - an AnnData object
            - type of linked element, 'shape' or 'point' 
            - the index of the linked element
        Example: 
            {'table': dummy_anndata.generate_dataset(n_obs=12, n_vars=20), 'element': 'shape', 'element_index': 0}

    Returns
    -------
    TableModel
        An TableModel object populated with random data according to the specified parameters.
    """

    if input is None:
        return None

    # add metadata to table
    region = input['element'] + '_' + str(input['element_index'])
    input['table'].obs['instance_id'] = input['table'].obs.index
    input['table'].obs['region'] = region
    input['table'].uns['spatialdata_attrs'] = {
        'region': region,
        'region_key': 'region',
        'instance_key': 'instance_id',
    }

    return TableModel.parse(input['table'])

# generate anndata
def generate_anndata(n_obs=12, n_vars=20):
    obs = pd.DataFrame(index=[f'obs_{i}' for i in range(n_obs)])
    var = pd.DataFrame(index=[f'var_{i}' for i in range(n_vars)])
    X = np.random.rand(n_obs, n_vars)
    adata = ad.AnnData(X=X, obs=obs, var=var)
    return adata