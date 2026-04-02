import dummy_spatialdata   
import pytest

from dummy_spatialdata import generate_transformations
from spatialdata.transformations import (
    Affine,
    Scale,
    Sequence,
    Translation,
    BaseTransformation, 
    Identity
)

def test_transformations():

    trans = generate_transformations({"trans_0": ["translation"]})
    assert isinstance(trans["trans_0"], Translation)

    trans = generate_transformations({"trans_0": ["scale"]})
    assert isinstance(trans["trans_0"], Scale)

    trans = generate_transformations({"trans_0": ["affine"]})
    assert isinstance(trans["trans_0"], Affine)

    trans = generate_transformations({"trans_0": ["translation", "scale", "affine"]})
    assert isinstance(trans["trans_0"], Sequence)