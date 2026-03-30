import os
import sys
import numpy as np
import spatialdata as sd

from pathlib import Path
from importlib.resources import files, as_file
from PIL import Image
from spatialdata.models import Image2DModel, ShapesModel, TableModel

def generate_dataset(
) -> sd.SpatialData:
    """Generate a dummy SpatialData object with specified elements.

    Parameters
    ----------
    n_obs : int, optional
        Number of observations (rows), by default 10.

    Returns
    -------
    sd.SpatialData
        A SpatialData object populated with random data according to the specified parameters.
    """

    resource = files("dummy_spatialdata").joinpath("examples", "bird.png")
    with as_file(resource) as path:
        img = np.array(Image.open(path))
    img = img.reshape(1, *img.shape)
    img_for_sdata = Image2DModel.parse(data=img, scale_factors=None)

    return img_for_sdata