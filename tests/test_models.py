import pytest

from dummy_spatialdata.generate_imagemodel import generate_imagemodel
from dummy_spatialdata.generate_labelmodel import generate_labelmodel
from dummy_spatialdata.generate_shapemodel import generate_shapemodel
from dummy_spatialdata.generate_pointmodel import generate_pointmodel
from dummy_spatialdata.generate_tablemodel import generate_tablemodel  
from spatialdata.models import Image2DModel, Labels2DModel, PointsModel, ShapesModel

import geopandas as gpd
import pandas as pd
import dask.dataframe as dd
import xarray

from spatialdata.transformations import (
    get_transformation,
    Affine,
    MapAxis,
    Scale,
    Sequence,
    Translation,
    BaseTransformation, 
    Identity
)

def test_shapemodel():

    # returns GeoDataFrame (circle)
    shp = generate_shapemodel({'n': 12, 'type': 'circle', 'coordinate_system': ['global']}, 'shape')
    assert isinstance(shp, gpd.GeoDataFrame)

    # returns GeoDataFrame (polygon)
    shp = generate_shapemodel({'n': 12, 'type': 'polygon', 'coordinate_system': ['global']}, 'shape')
    assert isinstance(shp, gpd.GeoDataFrame)

    # wrong shape type
    with pytest.raises(ValueError):
        shp = generate_shapemodel({'n': 12, 'type': 'art', 'coordinate_system': ['global']}, 'shape')

    # size is not defined
    with pytest.raises(KeyError):
        shp = generate_shapemodel({'type': 'circle', 'coordinate_system': ['global']}, 'shape')

    # no coordinate system returns element name as coord system and Identity transformation
    shp = generate_shapemodel({'n': 12, 'type': 'circle'}, 'shape')
    assert list(shp.attrs['transform'].keys())[0] == 'shape'
    assert get_transformation(shp, 'shape') == Identity()
    
    # parses coordinate system
    coord_system = {'global': {'transformations': ['affine'], 'shape': {'x': 2000, 'y': 2000}}}
    shp = generate_shapemodel({'n': 12, 'type': 'polygon', 'coordinate_system': ['global']}, 'image', coord_system)
    assert len(list(shp.attrs['transform'].keys())) == 1
    assert list(shp.attrs['transform'].keys())[0] == 'global'
    assert isinstance(get_transformation(shp, 'global'), Affine)

    # 'global' is the only coordinate system
    with pytest.raises(ValueError):
        get_transformation(shp, 'image')

def test_pointmodel():

    # returns DataFrame
    pts = generate_pointmodel({'n': 12, 'coordinate_system': ['global']}, 'image')
    assert isinstance(pts, dd.DataFrame)

    # size is not defined
    with pytest.raises(KeyError):
        pts = generate_pointmodel({'coordinate_system': ['global']}, 'image')

    # no coordinate system returns element name as coord system and Identity transformation
    pts = generate_pointmodel({'n': 12}, 'image')
    assert list(pts.attrs['transform'].keys())[0] == 'image'
    assert get_transformation(pts, 'image') == Identity()

    # parses coordinate system
    coord_system = {'global': {'transformations': ['affine'], 'shape': {'x': 2000, 'y': 2000}}}
    pts = generate_pointmodel({'n': 12, 'coordinate_system': ['global']}, 'image', coord_system)
    assert len(list(pts.attrs['transform'].keys())) == 1
    assert list(pts.attrs['transform'].keys())[0] == 'global'
    assert isinstance(get_transformation(pts, 'global'), Affine)

    # 'global' is the only coordinate system
    with pytest.raises(ValueError):
        get_transformation(pts, 'image')

def test_labelmodel():
    
    # returns DataFrame
    lbl = generate_labelmodel({'n': 12, 'scale_factors': [2,2,3], 'coordinate_system': ['global']}, 'image')
    assert isinstance(lbl, xarray.DataTree)
    assert len(lbl) == 4

    # size is not defined
    with pytest.raises(KeyError):
        lbl = generate_labelmodel({'coordinate_system': ['global']}, 'image')

    # single scale is returned for no scale factor definition
    lbl = generate_labelmodel({'n': 12, 'coordinate_system': ['global']}, 'image')
    assert len(lbl) == 1

    # no coordinate system returns element name as coord system and Identity transformation
    lbl = generate_labelmodel({'n': 12}, 'image')
    assert list(dict(lbl["scale0"])["image"].attrs["transform"].keys())[0] == 'image'
    assert get_transformation(lbl, 'image') == Identity()

    # parses coordinate system
    coord_system = {'global': {'transformations': ['affine'], 'shape': {'x': 2000, 'y': 2000}}}
    lbl = generate_labelmodel({'n': 12, 'coordinate_system': ['global']}, 'image', coord_system)
    assert len(list(dict(lbl["scale0"])["image"].attrs['transform'].keys())) == 1
    assert list(dict(lbl["scale0"])["image"].attrs['transform'].keys())[0] == 'global'
    assert isinstance(get_transformation(lbl, 'global'), Affine)

    # 'global' is the only coordinate system
    with pytest.raises(ValueError):
        get_transformation(lbl, 'image')