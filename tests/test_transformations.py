import pytest

from dummy_spatialdata import (
    generate_transformations, 
    get_basetransformations, 
    get_shape
)
from spatialdata.transformations import (
    Affine,
    MapAxis,
    Scale,
    Sequence,
    Translation,
    BaseTransformation, 
    Identity
)

def test_coordsystems():

    coordinate_systems = {
        'global': {'transformations': ['affine'], 'shape': {'x': 1000, 'y': 1000}},
        'global2': {'transformations': ['scale', 'translation'], 'shape':{'x': 1000, 'y': 1000}}
    }
        
    # get transformations of coordinate systems
    get_basetransformations(coordinate_systems)

    # get shapes of coordinate systems
    get_shape(coordinate_systems, 'global')
    
def test_empty_coordsystems():

    coordinate_systems = {}

    # get transformations of coordinate systems
    assert get_basetransformations(coordinate_systems)=={}

    # get shapes of coordinate systems
    assert get_shape(coordinate_systems, 'global')=={'x': 1000, 'y': 1000}

def wrong_coordsystems():

    coordinate_systems = {
        'global': {'transformations': ['affine'], 'shape': {'x': 1000, 'y': 1000}}
    }

    # unknown coordinate system
    with pytest.raises(ValueError):
        assert get_shape(coordinate_systems, 'global3')

def test_transformations():

    trans = generate_transformations({'global': {'transformations': ['identity'], 'shape': {'x': 1000, 'y': 1000}}})
    assert isinstance(trans['global'], Identity)

    trans = generate_transformations({'global': {'transformations': ['mapAxis'], 'shape': {'x': 1000, 'y': 1000}}})
    assert isinstance(trans['global'], MapAxis)

    trans = generate_transformations({'global': {'transformations': ['translation'], 'shape': {'x': 1000, 'y': 1000}}})
    assert isinstance(trans['global'], Translation)

    trans = generate_transformations({'global': {'transformations': ['scale'], 'shape': {'x': 1000, 'y': 1000}}})
    assert isinstance(trans['global'], Scale)

    trans = generate_transformations({'global3': {'transformations': ['rotation'], 'shape': {'x': 1000, 'y': 1000}}})
    assert isinstance(trans['global3'], Affine) # the rotation is basically returning an Affine transformation, for now

    trans = generate_transformations({'global3': {'transformations': ['affine'], 'shape': {'x': 1000, 'y': 1000}}})
    assert isinstance(trans['global3'], Affine)

    trans = generate_transformations({'global3': {'transformations': ['translation', 'scale', 'affine'], 'shape': {'x': 1000, 'y': 1000}}})
    assert isinstance(trans['global3'], Sequence)

    trans = generate_transformations({'global3': {'transformations': ['translation', 'mapAxis', 'scale', 'affine'], 'shape': {'x': 1000, 'y': 1000}}})
    assert isinstance(trans['global3'], Sequence)