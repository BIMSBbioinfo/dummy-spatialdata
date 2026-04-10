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
    coordinate_systems: Optional[dict] = None,
    SEED: Optional[int] = 42
) -> sd.SpatialData:
    """Generate a dummy SpatialData object with specified elements.

    Parameters
    ----------
    images: list[dict], optional
        A list of dictionaries, each specifying 
            - n: the type, either 'rgb' or 'grayscale' 
            - scale_factors: scale factors for the image pyramid (or a single image) 
            - coordinate_system: name of the coordinate_system (see 'coordinate_systems' parameter)
        Example: 
            [{'type': 'rgb', 'scale_factors': [2,2,2,2]}] or
            [{'type': 'grayscale', 'scale_factors': [2,2,2]}] or 
            [{'type': 'rgb', coordinate_system: 'global}, {'type': 'grayscale', 'scale_factors': [2,3]}]

    labels: list[dict], optional
        A list of dictionaries, each specifying 
            - n: number of labels, 
            - scale_factors: scale factors for the label mask pyramid (or a single mask) 
            - coordinate_system: name of the coordinate_system (see 'coordinate_systems' parameter)
        Example: 
            [{'n': 12, 'scale_factors': [2,2,2,2], 'coordinate_system': 'global'}]

    shapes: list[dict], optional
        A list of dictionaries, each specifying 
            - n: number of shapes, 
            - type: shape type, either 'polygon' or 'circle'
            - coordinate_system: name of the coordinate_system (see 'coordinate_systems' parameter)
        Example: 
            [{'n': 12, 'type': 'polygon', 'coordinate_system': 'global'}]

    points: list[dict], optional
        A list of dictionaries, each specifying 
            - n: number of points, 
            - coordinate_system: name of the coordinate_system (see 'coordinate_systems' parameter)
        Example: 
            [{'n': 12, 'coordinate_system': 'global'}]

    tables: list[AnnData], optional
        A list of dictionaries, each specifying
            - an AnnData object
            - type of linked element, 'shape' or 'point' 
            - the index of the linked element
        Example: 
            [{'table': dummy_anndata.generate_dataset(n_obs=12, n_vars=20), 'element': 'shape', 'element_index': 0}]
            [
                {'table': dummy_anndata.generate_dataset(n_obs=12, n_vars=20), 'element': 'shape', 'element_index': 0},
                {'table': dummy_anndata.generate_dataset(n_obs=20, n_vars=20), 'element': 'shape', 'element_index': 1}
            ]
    
    coordinate_systems: dict[dict]
        A dict of dictionaries, where keys are names of coordinate systems and each value specifying
            - a list of (or a single) transformation(s), 
            - shape of the input axes
        Example: 
            {
                'global': {'transformations': ['affine'], 'shape': {'x': 2000, 'y': 2000}},
                'global2': {'transformations': ['scale', 'translation'], 'shape':{'x': 500, 'y': 500}}
            },

    Returns
    -------
    sd.SpatialData
        A SpatialData object populated with custom elements according to the specified parameters.
    """
    
    # image model
    if images is None:
        images = {}
    else: 
        keys = [f'image_{i}' for i in range(len(images))]
        images = {key: generate_imagemodel(img, key, coordinate_systems) for img, key in zip(images, keys)}

    # label model
    if labels is None:
        labels = {}
    else: 
        keys = [f'label_{i}' for i in range(len(labels))]
        labels = {key: generate_labelmodel(lbl, key, coordinate_systems) for lbl, key in zip(labels, keys)}

    # shape model
    if shapes is None:
        shapes = {}
    else: 
        keys = [f'shape_{i}' for i in range(len(shapes))]
        shapes = {key: generate_shapemodel(shp, key, coordinate_systems, SEED) for shp, key in zip(shapes, keys)}

    # shape model
    if points is None:
        points = {}
    else: 
        keys = [f'point_{i}' for i in range(len(points))]
        points = {key: generate_pointmodel(shp, key, coordinate_systems, SEED) for shp, key in zip(points, keys)}

    # tables
    if tables is None:
        tables = {}
    else: 
        keys = [f'table_{i}' for i in range(len(tables))]
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
            region = tbl.uns['spatialdata_attrs']['region']
            element_type = region.split('_')[0]
            instance_key = tbl.uns['spatialdata_attrs']['instance_key']
            if region in sdata._shared_keys:
                element = getattr(sdata, element_type + 's')[region]
                tbl.obs['instance_id'] = element.index    

    return sdata