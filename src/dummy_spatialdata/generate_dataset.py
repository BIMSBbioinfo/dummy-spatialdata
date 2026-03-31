import os
import sys
import numpy as np
import spatialdata as sd

from pathlib import Path
from importlib.resources import files, as_file
from PIL import Image
from typing import Optional
from .generate_imagemodel import generate_imagemodel
from .generate_labelmodel import generate_labelmodel
from .generate_shapemodel import generate_shapemodel
from .generate_tablemodel import generate_tablemodel    
from spatialdata.models import TableModel

def generate_dataset(
    images: Optional[list] = None,
    labels: Optional[list] = None,
    shapes: Optional[list] = None,
    tables: Optional[list] = None,
    SEED: Optional[int] = 42
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
    if images is None:
        images = {}
    else: 
        images = [generate_imagemodel(img) for img in images]
        keys = [f"image_{i}" for i in range(len(images))]
        images = {key: img for key, img in zip(keys, images)}

    # label model
    if labels is None:
        labels = {}
    else: 
        labels = [generate_labelmodel(lbl) for lbl in labels]
        keys = [f"label_{i}" for i in range(len(labels))]
        labels = {key: lbl for key, lbl in zip(keys, labels)}

    # shape model
    if shapes is None:
        shapes = {}
    else: 
        shapes = [generate_shapemodel(shp, SEED) for shp in shapes]
        keys = [f"shape_{i}" for i in range(len(shapes))]
        shapes = {key: shp for key, shp in zip(keys, shapes)}

    # tables
    if tables is None:
        tables = {}
    else: 
        tables = [generate_tablemodel(tbl) for tbl in tables]
        keys = [f"table_{i}" for i in range(len(tables))]
        tables = {key: tbl for key, tbl in zip(keys, tables)}

    # create a SpatialData object and add the image data
    sdata = sd.SpatialData(
        images=images,
        labels=labels,
        shapes=shapes,
        tables=tables,
    )

    return sdata