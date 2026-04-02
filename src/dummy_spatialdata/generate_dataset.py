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
from .generate_pointmodel import generate_pointmodel
from .generate_tablemodel import generate_tablemodel    
from .generate_transformations import generate_transformations
from spatialdata.models import TableModel

def generate_dataset(
    images: Optional[list] = None,
    labels: Optional[list] = None,
    shapes: Optional[list] = None,
    points: Optional[list] = None,
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
        keys = [f"image_{i}" for i in range(len(images))]
        images = {key: generate_imagemodel(img, key) for img, key in zip(images, keys)}

    # label model
    if labels is None:
        labels = {}
    else: 
        keys = [f"label_{i}" for i in range(len(labels))]
        labels = {key: generate_labelmodel(lbl, key) for lbl, key in zip(labels, keys)}

    # shape model
    if shapes is None:
        shapes = {}
    else: 
        keys = [f"shape_{i}" for i in range(len(shapes))]
        shapes = {key: generate_shapemodel(shp, key, SEED) for shp, key in zip(shapes, keys)}

    # shape model
    if points is None:
        points = {}
    else: 
        keys = [f"point_{i}" for i in range(len(points))]
        points = {key: generate_pointmodel(shp, key, SEED) for shp, key in zip(points, keys)}

    # tables
    if tables is None:
        tables = {}
    else: 
        keys = [f"table_{i}" for i in range(len(tables))]
        tables = {key: generate_tablemodel(tbl) for tbl, key in zip(tables, keys)}

    # create a SpatialData object and add the image data
    sdata = sd.SpatialData(
        images=images,
        labels=labels,
        shapes=shapes,
        points=points,
        tables=tables,
    )

    # map shapes to tables
    if tables is not {}:
        for tbl in tables.values():
            region = tbl.uns["spatialdata_attrs"]["region"]
            element_type = region.split("_")[0]
            instance_key = tbl.uns["spatialdata_attrs"]["instance_key"]
            if region in sdata._shared_keys:
                element = getattr(sdata, element_type + "s")[region]
                tbl.obs['instance_id'] = element.index    

    return sdata