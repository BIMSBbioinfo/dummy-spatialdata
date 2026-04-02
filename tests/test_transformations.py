import dummy_spatialdata   
import pytest

from dummy_spatialdata import generate_transformations, get_coordsystem_transformations, get_coordsystem_shape
from spatialdata.transformations import (
    Affine,
    Scale,
    Sequence,
    Translation,
    BaseTransformation, 
    Identity
)

def test_coordsystems():

    coordinate_systems = {
        "global": {"transformations": ["affine"], "shape": {"x": 1000, "y": 1000}},
        "global2": {"transformations": ["scale", "translation"], "shape":{"x": 1000, "y": 1000}}
    }
        
    # get transformations of coordinate systems
    get_coordsystem_transformations(coordinate_systems)

    # get shapes of coordinate systems
    get_coordsystem_shape(coordinate_systems, "global")

def test_transformations():

    trans = generate_transformations({"global": {"transformations": ["translation"], "shape": {"x": 1000, "y": 1000}}})
    assert isinstance(trans["global"], Translation)

    trans = generate_transformations({"global": {"transformations": ["scale"], "shape": {"x": 1000, "y": 1000}}})
    assert isinstance(trans["global"], Scale)

    trans = generate_transformations({"global3": {"transformations": ["affine"], "shape": {"x": 1000, "y": 1000}}})
    assert isinstance(trans["global3"], Affine)

    trans = generate_transformations({"global3": {"transformations": ["translation", "scale", "affine"], "shape": {"x": 1000, "y": 1000}}})
    assert isinstance(trans["global3"], Sequence)