import os
import sys
import numpy as np
import spatialdata as sd

from pathlib import Path
from importlib.resources import files, as_file
from PIL import Image
from typing import Optional
from .generage_imagemodel import generate_imagemodel

def generate_dataset(
    images: Optional[list] = None,
) -> sd.SpatialData:
    """Generate a dummy SpatialData object with specified elements.

    Parameters
    ----------
    images: dict, optional
        A dictionary specifying the type and number of layers for the image data.
        Example: {"type": "rgb", "n_layers": 4} or {"type": "grayscale", "n_layers": 4}

    Returns
    -------
    sd.SpatialData
        A SpatialData object populated with random data according to the specified parameters.
    """
    
    # image model
    images = [generate_imagemodel(img) for img in images]
    keys = [f"image_{i}" for i in range(len(images))]
    images = {key: img for key, img in zip(keys, images)}

    # create a SpatialData object and add the image data
    sdata = sd.SpatialData(
        images=images,
        shapes={},
        tables={},
    )

    return sdata