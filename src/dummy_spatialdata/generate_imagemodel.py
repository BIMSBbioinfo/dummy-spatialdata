import os
import sys
import numpy as np

from pathlib import Path
from importlib.resources import files, as_file
from PIL import Image
from typing import Optional
from spatialdata.models import Image2DModel
from spatialdata.transformations import set_transformation, Identity
from .generate_transformations import generate_transformations, get_basetransformations, get_shape
from .utils import default_shape

def generate_imagemodel(
    input: Optional[dict] = None,
    key: Optional[str] = None,
    coordinate_systems: Optional[dict] = None
) -> Image2DModel:
    """Generate a dummy Image2DModel object with specified elements.

    Parameters
    ----------
    input : int, optional
        A dictionary of key value pairs with 
            - type: the type ('rgb', 'grayscale), 
            - scale_factors: Scale factors to apply to construct a multiscale image (datatree.DataTree). If None, a xarray.DataArray is returned instead. 
              Importantly, each scale factor is relative to the previous scale factor. For example, if the scale factors are [2, 2, 2], 
              the returned multiscale image will have 4 scales. The original image and then the 2x, 4x and 8x downsampled images.
            - coordinate_system: name of the coordinate_system (see 'coordinate_systems' parameter)
        Example: 
            {'type': 'rgb', 'scale_factors': (2,2,2,2)} or
            {'type': 'grayscale', 'scale_factors': (3,2), 'coordinate_systems': 'global'}
    
    key: str
        the name of the element

    coordinate_systems: 
        A set of coordinate systems

    Returns
    -------
    Image2DModel
        An Image2DModel object populated with random data according to the specified parameters.
    """

    # check input
    if input is None:
        return None
    
    # get shape
    input.update(
        {'shape': get_shape(coordinate_systems, 
                            input['coordinate_system'] if 'coordinate_system' in input else None)}
    )

    # get source 
    resource = files('dummy_spatialdata')

    # get image type
    if input['type'] == 'rgb':
        with as_file(resource.joinpath('examples', 'bird-color.png')) as path:
            img = Image.open(path)
            img = resize_image(img, input)
            img = np.array(img).astype(np.uint8)
        img = img.transpose((2, 0, 1))
    elif input['type'] == 'grayscale':
        with as_file(resource.joinpath('examples', 'nuclei.tif')) as path:
            img = Image.open(path)
            img = resize_image(img, input)
            img = np.array(img).astype(np.uint8)
        img = img.reshape(1, *img.shape)
    else:
        raise ValueError('Please type either \'rgb\' or \'grayscale\' for the image type.')   
    
    # get transformations
    coord_systems = get_basetransformations(coordinate_systems)
    if 'coordinate_system' in input:
        coord_system = input['coordinate_system']
        if coord_system in coord_systems:
            trans = {coord_system: coord_systems[coord_system]}
        else: 
            trans = {key: Identity()}
    else:
        trans = {key: Identity()}

    # image model
    if 'scale_factors' not in input:
        input["scale_factors"] = []
    imagemodel = Image2DModel.parse(data=img, 
                                    scale_factors=input['scale_factors'],
                                    transformations = trans)

    return imagemodel

def resize_image(image: Image, input: dict) -> Image:
    if 'shape' not in input:
        return image
    new_width = input['shape']['x']
    new_height = input['shape']['y']
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized